import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from readability import Document
from datetime import datetime
import yaml
import asyncio
from src.datasources.extractor import Extractor

class TheGuardianScraper(Extractor):
    def __init__(self) -> None:
        config = self.load_config()
        super().__init__(config)

    def load_config(self) -> str:
        with open('./src/config/scraper_config.yaml', 'r') as file:
            return yaml.safe_load(file)

    # Connection
    async def fetch(self, url: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                if response.status != 200:
                    raise Exception(f"HTTP request failed with {url}: {response.status}")
                return await response.text()

    # Returns all content data
    async def extract(self):
        try:
            main_page_content = await self.fetch(self.base_url)
            data = await self.parse(main_page_content)
            return data
        finally:
            await self.close()
    
    # Scraping Analysis
    async def parse(self, html_content: str):
        soup = BeautifulSoup(html_content, "html.parser")
        sections = soup.find_all('section')
        articles_info = []

        # Section informations
        for section in sections:
            section_title = section.get("id")
            if not section_title:
                continue
            
            # LI elements
            list_items = section.find_all('li')
            for li in list_items:
                # Article links elements
                article_link = li.find('a', href=True)
                href = article_link.get('href') if article_link else None

                # Construct the article url to get your content
                article_url = urljoin(self.base_url, href) if href else None

                # Footer element where contains the date
                footer = li.find('footer')
                time_tag = footer.find('time') if footer else None
                article_date = datetime.fromisoformat(
                    time_tag.get("datetime").replace('Z', '+00:00')
                ).strftime("%Y-%m-%d") if time_tag else None

                # Append basics informations
                articles_info.append({
                    "section": section_title,
                    "article_url": article_url,
                    "article_date": article_date
                })

        # Get planned information and execute each task
        tasks = [self.get_article_data(article) for article in articles_info]
        detailed_articles = await asyncio.gather(*tasks)

        # Merge basic and detailed informations
        for basic_info, detailed_info in zip(articles_info, detailed_articles):
            basic_info.update(detailed_info)

        # Return the merged data
        return articles_info

    async def get_article_data(self, article):
        url = article.get("article_url")
        if not url:
            return {"title": None, "content": None, "author": None}
        
        # Get the html content
        html_content = await self.fetch(url)

        # Readability to extract main content and article title
        doc = Document(html_content)
        title = doc.title()
        content = doc.summary()

        # Create a soup object to extract the author
        soup = BeautifulSoup(html_content, "html.parser")
        author_tag = soup.find('a', rel='author')
        author = author_tag.get_text(strip=True) if author_tag else None

        content_soup = BeautifulSoup(content, "html.parser")
        # Join the text of all paragraphs
        content_text = ' '.join([p.get_text(strip=True) for p in content_soup.find_all('p')])

        return {"title": title, "content": content_text, "author": author}
    
    async def close(self):
        if not self.session.closed:
            await self.session.close()