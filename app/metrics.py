
import requests
from urllib.parse import urlparse


def check_title_meta(pages):
    """Check title and meta description lengths."""

    results = []

    for page in pages:
        title = page.get("title", "")
        description = page.get("meta_description", "")

        results.append({
            "url": page["url"],
            "title": title,
            "title_length": len(title),
            "title_pass": 30 <= len(title) <= 60,
            "meta_description": description,
            "description_length": len(description),
            "description_pass": 70 <= len(description) <= 160
        })

    return results


def check_h1(pages):
    """Check whether each page has exactly one H1."""

    results = []

    for page in pages:
        headings = page.get("h1", [])

        results.append({
            "url": page["url"],
            "h1_count": len(headings),
            "h1_headings": headings,
            "pass": len(headings) == 1
        })

    return results


def check_image_alt(pages):
    """Check image alt attribute coverage."""

    total_images = 0
    images_with_alt = 0
    missing_alt = []

    for page in pages:
        images = page.get("images", [])

        for image in images:
            total_images += 1

            # Empty alt="" is still a valid alt attribute.
            if image.get("alt") is not None:
                images_with_alt += 1
            else:
                missing_alt.append({
                    "page": page["url"],
                    "image": image.get("src", "")
                })

    if total_images == 0:
        coverage = None
    else:
        coverage = round(
            (images_with_alt / total_images) * 100, 2
        )

    return {
        "total_images": total_images,
        "images_with_alt": images_with_alt,
        "missing_alt": missing_alt,
        "coverage_percentage": coverage
    }

def check_indexability(pages):
    """Check page status, noindex directives and canonical URLs."""

    results = []

    for page in pages:
        status = page.get("status_code")
        robots_meta = page.get("robots_meta", "").lower()
        canonical = page.get("canonical")

        issues = []

        if status != 200:
            issues.append(f"Page status is {status}")

        if "noindex" in robots_meta:
            issues.append("Page contains noindex directive")

        if not canonical:
            issues.append("Canonical tag is missing")

        indexable = (
            status == 200
            and "noindex" not in robots_meta
        )

        results.append({
            "url": page["url"],
            "status_code": status,
            "robots_meta": robots_meta,
            "canonical": canonical,
            "indexable_status": indexable,
            "issues": issues
        })

    return results


def check_broken_links(pages):
    """Check internal links and separate confirmed failures from unverified links."""
    from app.crawler import safe_get, get_domain

    broken_links = []
    unverified_links = []
    checked_links = set()

    MAX_LINKS_TO_CHECK = 30

    for page in pages:
        source_url = page["url"]

        for link in page.get("internal_links", []):
            if link in checked_links:
              continue

            if len(checked_links) >= MAX_LINKS_TO_CHECK:
               break

            checked_links.add(link)

            try:
                response = safe_get(
                    link,
                    allowed_domain=get_domain(source_url)
                )

                if response.status_code >= 400:
                    broken_links.append({
                        "url": link,
                        "source": source_url,
                        "status_code": response.status_code
                    })

            except Exception as error:
                unverified_links.append({
                    "url": link,
                    "source": source_url,
                    "error": str(error)
                })

    return {
        "total_links": len(checked_links),
        "broken_links": broken_links,
        "unverified_links": unverified_links
    }

def calculate_metrics(pages):

    return {
        "title_meta": check_title_meta(pages),
        "broken_links": check_broken_links(pages),
        "h1": check_h1(pages),
        "image_alt": check_image_alt(pages),
        "indexability": check_indexability(pages)
    }
