
def calculate_score(metrics, pages):
    """Calculate overall SEO score out of 100."""

    weights = {
        "title_meta": 25,
        "broken_links": 25,
        "h1": 15,
        "image_alt": 15,
        "indexability": 20
    }

    scores = {}

    # 1. Title and meta description
    title_results = metrics["title_meta"]

    if title_results:
        passed = sum(
            item["title_pass"] and item["description_pass"]
            for item in title_results
        )

        scores["title_meta"] = (
            passed / len(title_results)
        ) * 100
    else:
        scores["title_meta"] = None

    # 2. Broken links
    all_links = set()

    for page in pages:
        all_links.update(page.get("internal_links", []))

    broken_links = metrics["broken_links"]

    if all_links:
        scores["broken_links"] = (
            (len(all_links) - len(broken_links))
            / len(all_links)
        ) * 100
    else:
        scores["broken_links"] = None

    # 3. H1 headings
    h1_results = metrics["h1"]

    if h1_results:
        passed = sum(item["pass"] for item in h1_results)

        scores["h1"] = (
            passed / len(h1_results)
        ) * 100
    else:
        scores["h1"] = None

    # 4. Image alt text
    alt_data = metrics["image_alt"]

    scores["image_alt"] = alt_data["coverage_percentage"]

    # 5. Indexability
    index_results = metrics["indexability"]

    if index_results:
        passed = sum(
            item["indexable_status"]
            for item in index_results
        )

        scores["indexability"] = (
            passed / len(index_results)
        ) * 100
    else:
        scores["indexability"] = None

    # Calculate weighted score.
    # Metrics that cannot be measured are excluded.

    available_metrics = {
        name: value
        for name, value in scores.items()
        if value is not None
    }

    if not available_metrics:
        return {
            "overall_score": None,
            "metric_scores": scores
        }

    total_weight = sum(
        weights[name]
        for name in available_metrics
    )

    overall_score = sum(
        scores[name] * weights[name]
        for name in available_metrics
    ) / total_weight

    return {
        "overall_score": round(overall_score, 2),
        "metric_scores": {
            name: round(value, 2) if value is not None else None
            for name, value in scores.items()
        }
    }
