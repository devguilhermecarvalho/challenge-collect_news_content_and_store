from google.cloud import bigquery
from google.oauth2 import service_account

def get_bigquery_client():
    credentials_path = "./credentials/news-collect-and-store-22be09d2b3f9.json"
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = bigquery.Client(credentials=credentials)
    return client
