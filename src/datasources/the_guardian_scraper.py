from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import re
import asyncio
import yaml
from src.datasources.extractor import Extractor

class TheGuardianScraper(Extractor):
    def __init__(self):
        config = self.load_config()
        super().__init__(config)

    def load_config(self):
        with open('./src/config/scraper_config.yaml', 'r') as file:
            return yaml.safe_load(file)

    async def parse(self, html_content: str):
        soup = BeautifulSoup(html_content, "html.parser")
        sections = soup.find_all('section')
        articles_info = []

        for section in sections:
            section_title = section.get("id")
            if not section_title:
                continue

            list_items = section.find_all('li')
            for li in list_items:
                article_link = li.find('a', href=True)
                href = article_link.get('href') if article_link else None
                article_url = urljoin(self.base_url, href) if href else None

                footer = li.find('footer')
                time_tag = footer.find('time') if footer else None
                article_date = datetime.fromisoformat(
                    time_tag.get("datetime").replace('Z', '+00:00')
                ).strftime("%Y-%m-%d") if time_tag else None

                articles_info.append({
                    "section": section_title,
                    "article_url": article_url,
                    "article_date": article_date
                })

        tasks = [self.get_article_data(article) for article in articles_info]
        detailed_articles = await asyncio.gather(*tasks)
        for basic_info, detailed_info in zip(articles_info, detailed_articles):
            basic_info.update(detailed_info)

        return articles_info

    async def get_article_data(self, article):
        url = article.get("article_url")
        if not url:
            return {"title": None, "subtitle": None, "content": None, "author": None}
        
        html_content = await self.fetch(url)
        soup = BeautifulSoup(html_content, "html.parser")

        title_tag = soup.find('h1', class_=re.compile(r"dcr-"))
        title = title_tag.get_text(strip=True) if title_tag else None

        subtitle_tag = soup.find('div', class_=re.compile(r"dcr-"))
        subtitle = subtitle_tag.get_text(strip=True) if subtitle_tag else None

        content_div = soup.find('div', class_=re.compile(r"article-body-commercial-selector"))
        if content_div:
            content_paragraphs = content_div.find_all('p', class_=re.compile(r"dcr-"))
            content = ' '.join([p.get_text(strip=True) for p in content_paragraphs])
        else:
            content = None

        author_tag = soup.find('a', rel='author')
        author = author_tag.get_text(strip=True) if author_tag else None

        return {"title": title, "subtitle": subtitle, "content": content, "author": author}