
import ipaddress
import socket
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urldefrag
from urllib.robotparser import RobotFileParser
from collections import deque



MAX_PAGES = 10
TIMEOUT = 5

HEADERS = {
    "User-Agent": "SEOPulseBot/1.0 (educational SEO audit)"
}


def normalize_url(url):
    """Remove URL fragments without changing the path."""
    url, _ = urldefrag(url)
    return url

def get_domain(url):
    """Return the website domain."""
    return urlparse(url).netloc.lower()




def is_valid_url(url):
    """Validate HTTP URLs and reject private or unsafe destinations."""

    parsed = urlparse(url)

    if (
        parsed.scheme not in ("http", "https")
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
    ):
        return False

    hostname = parsed.hostname.lower()

    if hostname == "localhost" or hostname.endswith(".localhost"):
        return False

    try:
        addresses = socket.getaddrinfo(
            hostname,
            None,
            type=socket.SOCK_STREAM
        )

        for address in addresses:
            ip = ipaddress.ip_address(address[4][0])

            if (
                ip.is_private
                or ip.is_loopback
                or ip.is_link_local
                or ip.is_reserved
                or ip.is_multicast
                or ip.is_unspecified
            ):
                return False

        return bool(addresses)

    except (socket.gaierror, ValueError, OSError):
        return False


def safe_get(url, allowed_domain=None, max_redirects=5):
    """Fetch a URL while manually checking redirects."""

    current_url = url
    visited_urls = set()

    for _ in range(max_redirects + 1):

        if current_url in visited_urls:
            raise ValueError("Redirect loop detected.")

        visited_urls.add(current_url)

        if not is_valid_url(current_url):
            raise ValueError("Unsafe URL blocked.")

        current_domain = get_domain(current_url)

        if allowed_domain is not None:
            current_domain_clean = current_domain.lower().removeprefix("www.")
            allowed_domain_clean = allowed_domain.lower().removeprefix("www.")

            if current_domain_clean != allowed_domain_clean:
                raise ValueError("Redirect outside the allowed domain.")

        response = requests.get(
            current_url,
            headers=HEADERS,
            timeout=TIMEOUT,
            allow_redirects=False
        )

        if response.status_code not in (301, 302, 303, 307, 308):
            return response

        location = response.headers.get("Location")

        if not location:
            return response

        current_url = normalize_url(
            urljoin(current_url, location)
        )

    raise ValueError("Too many redirects.")


def check_robots(start_url):
    """Check whether our crawler is allowed by robots.txt."""

    parsed = urlparse(start_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    robot_parser = RobotFileParser()
    robot_parser.set_url(robots_url)

    try:
        response = safe_get(
            robots_url,
            allowed_domain=get_domain(start_url)
        )

        if response.status_code >= 400:
            return None

        robot_parser.parse(response.text.splitlines())
        return robot_parser

    except (requests.RequestException, ValueError, OSError):
        return None

def crawl_website(start_url):
    """Crawl pages on the same website and collect SEO data."""

    start_url = normalize_url(start_url)

    if not is_valid_url(start_url):
        raise ValueError("Please enter a valid HTTP or HTTPS URL.")

    domain = get_domain(start_url)
    robots = check_robots(start_url)

    if robots is None:
        raise ValueError(
            "Could not safely verify robots.txt. "
            "The crawl was stopped."
        )

    queue = deque([start_url])
    visited = set()
    pages = []

    while queue and len(visited) < MAX_PAGES:

        current_url = queue.popleft()

        if current_url in visited:
            continue

        if not is_valid_url(current_url):
            continue

        if get_domain(current_url) != domain:
            continue

        if not robots.can_fetch(HEADERS["User-Agent"], current_url):
            continue

        visited.add(current_url)

        try:
            response = safe_get(
                current_url,
                allowed_domain=domain
            )

            page_data = {
                "url": current_url,
                "status_code": response.status_code,
                "title": "",
                "meta_description": "",
                "h1": [],
                "images": [],
                "internal_links": [],
                "canonical": None,
                "robots_meta": ""
            }

            if (
                response.status_code == 200
                and "text/html" in response.headers.get(
                    "Content-Type", ""
                ).lower()
            ):

                soup = BeautifulSoup(response.text, "html.parser")

                # Extract title
                if soup.title:
                    page_data["title"] = soup.title.get_text(
                        strip=True
                    )

                # Extract meta description
                meta = soup.find(
                    "meta",
                    attrs={
                        "name": lambda value:
                        value and value.lower() == "description"
                    }
                )

                if meta:
                    page_data["meta_description"] = meta.get(
                        "content", ""
                    ).strip()

                # Extract canonical URL
                canonical_tag = soup.find(
                    "link",
                    rel="canonical"
                )

                if canonical_tag:
                    page_data["canonical"] = urljoin(
                        current_url,
                        canonical_tag.get("href", "")
                    )

                # Extract robots meta tag
                robots_tag = soup.find(
                    "meta",
                    attrs={
                        "name": lambda value:
                        value and value.lower() == "robots"
                    }
                )

                if robots_tag:
                    page_data["robots_meta"] = robots_tag.get(
                        "content", ""
                    ).lower()

                # Extract H1 headings
                page_data["h1"] = [
                    h.get_text(strip=True)
                    for h in soup.find_all("h1")
                ]

                # Extract images
                page_data["images"] = [
                    {
                        "src": urljoin(
                            current_url,
                            img.get("src", "")
                        ),
                        "alt": img.get("alt")
                    }
                    for img in soup.find_all("img")
                ]

                # Extract internal links
                for anchor in soup.find_all("a", href=True):

                    link = normalize_url(
                        urljoin(current_url, anchor["href"])
                    )

                    if (
                        is_valid_url(link)
                        and get_domain(link) == domain
                    ):
                        page_data["internal_links"].append(link)

                        if (
                            link not in visited
                            and link not in queue
                            and len(visited) + len(queue) < MAX_PAGES
                        ):
                            queue.append(link)

            pages.append(page_data)

        except (requests.RequestException, ValueError, OSError) as error:

            pages.append({
                "url": current_url,
                "status_code": None,
                "error": str(error),
                "title": "",
                "meta_description": "",
                "h1": [],
                "images": [],
                "internal_links": [],
                "canonical": None,
                "robots_meta": ""
            })

    return pages