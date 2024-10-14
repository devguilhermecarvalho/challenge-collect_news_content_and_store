import pandas as pd

class TheGuardianTransformer:
    def __init__(self):
        pass

    def transform(self, data):
        df = pd.DataFrame(data)
        df = self.clean_data(df)
        df = self.validate_data(df)
        df = self.validate_author(df)
        df = self.transform_data_types(df)

        return df

    def clean_data(self, df):
        df = df.drop_duplicates()
        if 'subtitle' in df.columns:
            df = df.drop(columns=['subtitle'])
        return df

    def validate_data(self, df):
        df = df.dropna(subset=['title', 'content'])
        return df
    
    def validate_author(self, df):
        df['author'] = df['author'].fillna('Author Unknown')
        return df

    def transform_data_types(self, df):
        df['article_date'] = pd.to_datetime(df['article_date'], errors='coerce')
        df['article_date'] = df['article_date'].fillna(pd.to_datetime('today').date())
        return df