# src/processors/the_guardian_processor.py

import pandas as pd
import os
from datetime import datetime

class TheGuardianProcessor:
    def __init__(self, config):
        self.output_dir = config["output_path"]

    def process(self, data):
        df = pd.DataFrame(data)
        df = self.clean_subtitle_from_content(df)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        output_file = os.path.join(self.output_dir, f"theguardian_articles_{timestamp}.csv")

        os.makedirs(self.output_dir, exist_ok=True)
        df.to_csv(output_file, index=False)

        return output_file

    def clean_subtitle_from_content(self, df):
        def clean_row(row):
            subtitle = str(row['subtitle']).strip()
            content = str(row['content']).strip()
            if not subtitle or not content:
                return row
            row['content'] = content.replace(subtitle, '', 1).strip()
            return row
        return df.apply(clean_row, axis=1)
