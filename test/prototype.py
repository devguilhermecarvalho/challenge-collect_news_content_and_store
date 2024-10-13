import asyncio
import aiohttp
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from urllib.parse import urljoin
import re

# Classe responsável por gerenciar as requisições HTTP
class HTTPClient:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def fetch(self, url: str) -> str:
        """
        Faz uma requisição HTTP GET para a URL especificada e retorna o conteúdo HTML.

        :param url: URL da página a ser requisitada.
        :return: Conteúdo HTML da resposta.
        """
        async with self.session.get(url) as response:
            response.raise_for_status()
            return await response.text()

    async def close(self):
        """
        Encerra a sessão HTTP.
        """
        await self.session.close()

# Classe abstrata que define a interface para um scraper de notícias
class NewsScraper(ABC):
    @abstractmethod
    async def fetch_page(self, url: str) -> str:
        """
        Obtém o conteúdo HTML de uma página.

        :param url: URL da página.
        :return: Conteúdo HTML da página.
        """
        pass

    @abstractmethod
    async def parse_page(self, html_content: str) -> BeautifulSoup:
        """
        Analisa o conteúdo HTML e retorna um objeto BeautifulSoup.

        :param html_content: Conteúdo HTML da página.
        :return: Objeto BeautifulSoup analisado.
        """
        pass

    @abstractmethod
    async def extract_articles(self, soup: BeautifulSoup):
        """
        Extrai as informações dos artigos da página analisada.

        :param soup: Objeto BeautifulSoup da página.
        :return: Lista de informações dos artigos.
        """
        pass

    @abstractmethod
    async def get_article_data(self, url: str):
        """
        Obtém os dados detalhados de um artigo específico.

        :param url: URL do artigo.
        :return: Dicionário com os dados do artigo.
        """
        pass

# Classe que implementa o scraper para o site The Guardian
class TheGuardianScraper(NewsScraper):
    def __init__(self, base_url: str, http_client: HTTPClient):
        self.base_url = base_url
        self.http_client = http_client

    async def fetch_page(self, url: str) -> str:
        """
        Obtém o conteúdo HTML da página especificada.

        :param url: URL da página.
        :return: Conteúdo HTML da página.
        """
        return await self.http_client.fetch(url)

    async def parse_page(self, html_content: str) -> BeautifulSoup:
        """
        Analisa o conteúdo HTML e retorna um objeto BeautifulSoup.

        :param html_content: Conteúdo HTML da página.
        :return: Objeto BeautifulSoup analisado.
        """
        return BeautifulSoup(html_content, "html.parser")

    async def extract_sections(self, soup: BeautifulSoup):
        """
        Extrai as seções da página principal.

        :param soup: Objeto BeautifulSoup da página principal.
        :return: Lista de seções encontradas.
        """
        return soup.find_all('section')

    async def extract_articles(self, sections):
        """
        Extrai as informações básicas dos artigos listados nas seções.

        :param sections: Lista de seções da página.
        :return: Lista de dicionários com informações básicas dos artigos.
        """
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

                # Extrai a data do artigo
                footer = li.find('footer')
                time_tag = footer.find('time') if footer else None
                if time_tag and time_tag.get("datetime"):
                    date_str = time_tag.get("datetime").replace('Z', '+00:00')
                    article_date = datetime.fromisoformat(date_str).strftime("%Y-%m-%d")
                else:
                    article_date = None

                articles_info.append({
                    "section": section_title,
                    "article_url": article_url,
                    "article_date": article_date
                })

        return articles_info

    async def get_article_data(self, url: str):
        """
        Obtém os dados detalhados de um artigo a partir da sua URL.

        :param url: URL do artigo.
        :return: Dicionário com dados do artigo.
        """
        if not url:
            return {
                "title": None,
                "subtitle": None,
                "content": None,
                "author": None,
                "author_profile_link": None
            }

        try:
            html_content = await self.fetch_page(url)
        except Exception:
            return {
                "title": None,
                "subtitle": None,
                "content": None,
                "author": None,
                "author_profile_link": None
            }

        soup = await self.parse_page(html_content)

        # Extrai o título
        title_tag = soup.find('h1', class_=re.compile(r"dcr-"))
        title = title_tag.get_text(strip=True) if title_tag else None

        # Extrai o subtítulo
        subtitle = None
        subtitle_tag = soup.find('div', class_=re.compile(r"dcr-"))
        if subtitle_tag and any('standfirst' in cls for cls in subtitle_tag.get('class', [])):
            subtitle = subtitle_tag.get_text(strip=True)

        # Extrai o conteúdo do artigo
        content = None
        content_div = soup.find('div', class_=re.compile(r"article-body-commercial-selector"))
        if content_div:
            content_paragraphs = content_div.find_all('p', class_=re.compile(r"dcr-"))
            content = ' '.join([p.get_text(strip=True) for p in content_paragraphs])

        # Extrai o autor
        author_tag = soup.find('a', rel='author')
        author_name = author_tag.get_text(strip=True) if author_tag else None
        author_profile_link = author_tag.get('href') if author_tag else None

        return {
            "title": title,
            "subtitle": subtitle,
            "content": content,
            "author": author_name,
            "author_profile_link": author_profile_link
        }

    async def scrape(self):
        """
        Executa o processo de scraping completo e retorna os dados estruturados.

        :return: Lista de dicionários com os dados dos artigos.
        """
        # Obtém o conteúdo da página principal
        main_page_content = await self.fetch_page(self.base_url)
        soup = await self.parse_page(main_page_content)

        # Extrai as seções da página
        sections = await self.extract_sections(soup)
        articles_info = await self.extract_articles(sections)

        # Lista para armazenar as tarefas de obtenção de dados dos artigos
        tasks = []
        for article in articles_info:
            article_url = article.get("article_url")
            tasks.append(self.get_article_data(article_url))

        # Executa as tarefas de forma assíncrona
        articles_data = await asyncio.gather(*tasks)

        # Combina as informações básicas com os dados detalhados dos artigos
        for article_info, article_data in zip(articles_info, articles_data):
            article_info.update(article_data)

        return articles_info

# Função para remover o subtítulo do conteúdo
def clean_subtitle_from_content(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove o subtítulo do início do conteúdo do artigo, se presente.

    :param df: DataFrame com os dados dos artigos.
    :return: DataFrame atualizado com o conteúdo limpo.
    """
    def clean_row(row):
        subtitle = str(row['subtitle']).strip()
        content = str(row['content']).strip()

        if not subtitle or not content:
            return row

        # Remove o subtítulo do início do conteúdo
        pattern = r'^' + re.escape(subtitle) + r'\s*'
        row['content'] = re.sub(pattern, '', content)
        return row

    return df.apply(clean_row, axis=1)

# Função principal
async def main():
    """
    Função principal que coordena o processo de scraping e processamento dos dados.
    """
    base_url = "https://www.theguardian.com/au"
    http_client = HTTPClient()
    scraper = TheGuardianScraper(base_url=base_url, http_client=http_client)

    try:
        # Executa o scraping e obtém os dados
        data = await scraper.scrape()

        # Converte os dados em um DataFrame
        df = pd.DataFrame(data)

        # Limpa o conteúdo removendo o subtítulo duplicado
        df = clean_subtitle_from_content(df)

        # Salva os dados em um arquivo CSV
        df.to_csv('./test/data/theguardian_articles.csv', index=False)
    finally:
        # Encerra a sessão HTTP
        await http_client.close()

# Executa a função principal
if __name__ == "__main__":
    asyncio.run(main())