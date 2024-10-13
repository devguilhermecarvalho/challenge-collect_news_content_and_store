import asyncio
from src.datasources.factory import ScraperFactory

async def main():
    factory = ScraperFactory()
    scraper = factory.get_scraper("the_guardian")
    await scraper.extract()

if __name__ == "__main__":
    asyncio.run(main())