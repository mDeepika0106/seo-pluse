from app.metrics import (
    check_title_meta,
    check_h1,
    check_image_alt,
    check_indexability
)


def sample_pages():
    return [
        {
            "url": "https://example.com",
            "status_code": 200,
            "title": "Example Website Title Here",
            "meta_description": "This is a sample description for testing purposes.",
            "h1": ["Welcome"],
            "images": [
                {"src": "image1.jpg", "alt": "Sample image"},
                {"src": "image2.jpg", "alt": ""}
            ],
            "internal_links": [],
            "canonical": "https://example.com",
            "robots_meta": ""
        }
    ]


def test_title_meta():
    results = check_title_meta(sample_pages())
    assert len(results) == 1
    assert results[0]["title_length"] == len(
        "Example Website Title Here"
    )


def test_h1():
    results = check_h1(sample_pages())
    assert results[0]["h1_count"] == 1
    assert results[0]["pass"] is True


def test_image_alt():
    result = check_image_alt(sample_pages())
    assert result["total_images"] == 2
    assert result["images_with_alt"] == 2
    assert result["coverage_percentage"] == 100.0


def test_indexability():
    results = check_indexability(sample_pages())
    assert results[0]["indexable_status"] is True
    assert results[0]["issues"] == []


def test_noindex_page():
    pages = sample_pages()
    pages[0]["robots_meta"] = "noindex"

    results = check_indexability(pages)

    assert results[0]["indexable_status"] is False
    assert "Page contains noindex directive" in results[0]["issues"]

    def test_missing_h1():
        pages = sample_pages()
        pages[0]["h1"] = []

        results = check_h1(pages)

        assert results[0]["h1_count"] == 0
        assert results[0]["pass"] is False


def test_no_images():
        pages = sample_pages()
        pages[0]["images"] = []

        result = check_image_alt(pages)

        assert result["total_images"] == 0
        assert result["coverage_percentage"] is None