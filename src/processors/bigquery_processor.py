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
            self.client.get_table(table_ref)  # Tenta obter a tabela
            print(f"Tabela {table_ref} já existe.")
        except NotFound:
            print(f"Tabela {table_ref} não encontrada. Criando tabela...")
            schema = self.get_table_schema()
            table = bigquery.Table(table_ref, schema=schema)
            self.client.create_table(table)
            print(f"Tabela {table_ref} criada com sucesso.")

    def get_existing_articles(self):
        table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"
        query = f"SELECT article_url FROM `{table_ref}`"
        query_job = self.client.query(query)
        existing_articles = query_job.result().to_dataframe()
        return existing_articles

    def process(self, data: pd.DataFrame):
        if data is None or data.empty:
            print.warning("Nenhum dado foi recebido para processamento.")
            return None

        df = data.copy()

        if df.empty:
            print.warning("O DataFrame está vazio. Nenhum dado para enviar ao BigQuery.")
            return None

        self.ensure_table_exists()

        existing_articles = self.get_existing_articles()

        if not existing_articles.empty:
            df = df[~df['article_url'].isin(existing_articles['article_url'])]

        if df.empty:
            print("Nenhum novo artigo para inserir.")
            return None

        schema = self.get_table_schema()

        table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"

        job_config = bigquery.LoadJobConfig(
            schema=schema,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )

        try:
            job = self.client.load_table_from_dataframe(df, table_ref, job_config=job_config)
            job.result()
            print(f"Inserção concluída na tabela {table_ref}")
            return table_ref
        except Exception as e:
            print(f"Erro ao inserir dados no BigQuery: {e}")
            return None