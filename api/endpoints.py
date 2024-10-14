from fastapi import APIRouter, Query
from google.cloud import bigquery
from api.config import get_bigquery_client

router = APIRouter()

@router.get("/articles")
async def get_articles(keyword: str = Query(None, description="Palavra-chave para buscar nos títulos")):
    client = get_bigquery_client()
    
    # Monta a query SQL
    query = """
        SELECT title, author, article_url, article_date, section, content
        FROM `news-collect-and-store.scraping_results.raw_the_guardian_news`
    """
    
    if keyword:
        query += f" WHERE LOWER(content) LIKE '%{keyword.lower()}%'"

    query += " LIMIT 10"

    query_job = client.query(query)
    articles = query_job.result().to_dataframe().to_dict(orient="records")
    
    return {"articles": articles}