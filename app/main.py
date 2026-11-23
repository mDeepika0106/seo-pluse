
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

from app.crawler import crawl_website
from app.metrics import calculate_metrics
from app.scoring import calculate_score
from app.ai_recommendations import generate_recommendations


app = FastAPI(
    title="AI Marketing Intelligence Assistant",
    description="Website SEO auditing and AI recommendations",
    version="1.0"
)


class AuditRequest(BaseModel):
    url: HttpUrl


@app.get("/")
def home():
    return {
        "message": "AI Marketing Intelligence Assistant is running!"
    }


@app.post("/audit")
def audit_website(request: AuditRequest):

    url = str(request.url)

    try:
        # Step 1: Crawl the website
        pages = crawl_website(url)

        if not pages:
            raise HTTPException(
                status_code=400,
                detail="No pages could be crawled."
            )

        # Step 2: Calculate SEO metrics
        metrics = calculate_metrics(pages)

        # Step 3: Calculate SEO score
        score = calculate_score(metrics, pages)

        # Step 4: Prepare audit data for AI
        audit_data = {
            "website": url,
            "pages_crawled": len(pages),
            "metrics": metrics,
            "score": score
        }

        # Step 5: Generate AI recommendations
        recommendations = generate_recommendations(
            audit_data
        )

        # Step 6: Return results
        return {
            "website": url,
            "pages_crawled": len(pages),
            "metrics": metrics,
            "score": score,
            "recommendations": recommendations
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Audit failed: {str(error)}"
        )
