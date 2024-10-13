from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

class BigQueryProcessor:
    def __init__(self, config):
        self.project_id = config["project_id"]
        self.dataset_id = config["dataset_id"]
        self.table_id = config["table_id"]
        self.credentials_path = config["credentials_path"]

        # Carregar as credenciais de serviço
        self.credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
        self.client = bigquery.Client(project=self.project_id, credentials=self.credentials)

    def get_existing_articles(self):
        query = f"""
        SELECT article_url FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`
        """
        query_job = self.client.query(query)
        existing_articles = query_job.result().to_dataframe()  # Converter o resultado em DataFrame
        return existing_articles

    def process(self, data):
        # Verificar se os dados foram recebidos corretamente
        if data is None or data.empty:
            print("Nenhum dado foi recebido para processamento.")
            return None

        # Criar o DataFrame
        df = pd.DataFrame(data)

        # Verificar se o DataFrame está vazio
        if df.empty:
            print("O DataFrame está vazio. Nenhum dado para enviar ao BigQuery.")
            return None

        # Obter URLs já presentes no BigQuery
        existing_articles = self.get_existing_articles()
        print(f"Artigos existentes no BigQuery: {len(existing_articles)}")

        # Filtrar os novos artigos, que ainda não estão no BigQuery
        new_articles = df[~df['article_url'].isin(existing_articles['article_url'])]

        if new_articles.empty:
            print("Nenhum novo artigo encontrado para inserção.")
            return None

        print(f"Novos artigos a serem inseridos: {len(new_articles)}")

        # Converter colunas para tipos apropriados
        new_articles.loc[:, 'article_date'] = pd.to_datetime(new_articles['article_date']).dt.date

        # Definir o esquema explicitamente
        schema = [
            bigquery.SchemaField("title", "STRING"),
            bigquery.SchemaField("subtitle", "STRING"),
            bigquery.SchemaField("content", "STRING"),
            bigquery.SchemaField("author", "STRING"),
            bigquery.SchemaField("article_url", "STRING"),
            bigquery.SchemaField("article_date", "DATE"),
            bigquery.SchemaField("section", "STRING")
        ]

        table_ref = f"{self.project_id}.{self.dataset_id}.{self.table_id}"

        # Configurar o job de carregamento com o esquema e a política de gravação
        job_config = bigquery.LoadJobConfig(
            schema=schema,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,  # Manter os dados existentes
        )

        # Executar o job de carregamento
        job = self.client.load_table_from_dataframe(new_articles, table_ref, job_config=job_config)
        job.result()  # Aguarda a conclusão da inserção

        print(f"Inserção concluída na tabela {table_ref}")
        return table_ref
