import aiohttp
from abc import ABC, abstractmethod
import pandas as pd
import os
from datetime import datetime

class Extractor(ABC):
    def __init__(self, config):
        self.base_url = config["the_guardian_url"]
        self.output_dir = config["output_path"]
        self.session = aiohttp.ClientSession()

    async def fetch(self, url: str) -> str:
        async with self.session.get(url) as response:
            response.raise_for_status()
            return await response.text()

    @abstractmethod
    async def parse(self, html_content: str):
        pass

    async def extract(self):
        try:
            main_page_content = await self.fetch(self.base_url)
            data = await self.parse(main_page_content)
            df = pd.DataFrame(data)
            df = self.clean_subtitle_from_content(df)
            os.makedirs(self.output_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            output_file = os.path.join(self.output_dir, f"theguardian_articles_{timestamp}.csv")
            df.to_csv(output_file, index=False)
        finally:
            await self.close()

    async def close(self):
        await self.session.close()

    def clean_subtitle_from_content(self, df):
        def clean_row(row):
            subtitle = str(row['subtitle']).strip()
            content = str(row['content']).strip()
            if not subtitle or not content:
                return row
            row['content'] = content.replace(subtitle, '', 1).strip()
            return row
        return df.apply(clean_row, axis=1)
