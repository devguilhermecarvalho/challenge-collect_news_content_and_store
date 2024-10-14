from fastapi import APIRouter
from google.cloud import bigquery
from api.config import get_bigquery_client

router = APIRouter()

@router.get("/articles")
async def get_articles():
    client = get_bigquery_client()
    query = """
        SELECT title, author, article_url, article_date, section, content
        FROM `news-collect-and-store.scraping_results.raw_the_guardian_news`
        LIMIT 30
    """

    query_job = client.query(query, location="US")
    articles = query_job.result().to_dataframe().to_dict(orient="records")
    return {"articles": articles}
