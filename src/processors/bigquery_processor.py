from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
from typing import Any, Dict
from google.api_core.exceptions import NotFound


class BigQueryProcessor:
    def __init__(self, config: Dict[str, Any]):
        self.project_id = config["project_id"]
        self.dataset_id = config["dataset_id"]
        self.table_id = config["table_id"]
        self.credentials_path = config["credentials_path"]

        self.credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
        self.client = bigquery.Client(project=self.project_id, credentials=self.credentials)

    def get_table_schema(self):
        schema = [
            bigquery.SchemaField("title", "STRING"),
            bigquery.SchemaField("content", "STRING"),
            bigquery.SchemaField("author", "STRING"),
            bigquery.SchemaField("article_url", "STRING"),
            bigquery.SchemaField("article_date", "DATE"),
            bigquery.SchemaField("section", "STRING")
        ]
        return schema

    def ensure_table_exists(self):
        table_ref = self.client.dataset(self.dataset_id).table(self.table_id)
        try:
            self.client.get_table(table_ref)
            print(f"Connected to BigQuery: {table_ref}")
        except NotFound:
            print(f"The table {table_ref} not found. Creating table...")
            schema = self.get_table_schema()
            table = bigquery.Table(table_ref, schema=schema)
            self.client.create_table(table)
            print(f"The table {table_ref} successfully created.")

    def get_existing_articles(self):
        table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"
        query = f"SELECT article_url FROM `{table_ref}`"
        query_job = self.client.query(query)
        existing_articles = query_job.result().to_dataframe()
        return existing_articles

    def process(self, data: pd.DataFrame):
        if data is None or data.empty:
            print("No data was received for processing.")
            return None

        df = data.copy()

        if df.empty:
            print("The DataFrame is empty. No data to send to BigQuery.")
            return None

        self.ensure_table_exists()

        existing_articles = self.get_existing_articles()

        if not existing_articles.empty:
            df = df[~df['article_url'].isin(existing_articles['article_url'])]

        print(f"Existing articles on BigQuery: {len(existing_articles)}")

        if df.empty:
            print("No new articles found for insertion.")
            return None

        print(f"New articles to be inserted: {len(df)}")

        schema = self.get_table_schema()

        table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"

        job_config = bigquery.LoadJobConfig(
            schema=schema,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )

        try:
            job = self.client.load_table_from_dataframe(df, table_ref, job_config=job_config)
            job.result()
            print(f"Inserted data into the table successfully. {table_ref}")
            return table_ref
        except Exception as e:
            print(f"Error inserting data into BigQuery: {e}")
            return None