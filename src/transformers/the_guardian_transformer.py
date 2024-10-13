# src/transformers/the_guardian_transformer.py

import pandas as pd

class TheGuardianTransformer:
    def __init__(self):
        pass

    def transform(self, data):
        # Criar DataFrame a partir dos dados extraídos
        df = pd.DataFrame(data)

        # Passo 1: Limpeza de dados
        df = self.clean_data(df)

        # Passo 2: Validação de dados
        df = self.validate_data(df)

        # Passo 3: Transformação de tipos
        df = self.transform_data_types(df)

        return df

    def clean_data(self, df):
        # Remover duplicatas
        df = df.drop_duplicates()

        # Preencher valores nulos em colunas não obrigatórias usando .loc
        df.loc[:, 'subtitle'] = df['subtitle'].fillna('')

        return df

    def validate_data(self, df):
        # Remover linhas onde o título ou conteúdo estejam ausentes
        df = df.dropna(subset=['title', 'content'])

        return df

    def transform_data_types(self, df):
        # Converter datas para o tipo correto
        df['article_date'] = pd.to_datetime(df['article_date'], errors='coerce').dt.date

        return df