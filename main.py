# main

import asyncio
from src.datasources.factory import ScraperFactory
from src.processors.processor_factory import ProcessorFactory
from src.transformers.transformer_factory import TransformerFactory

async def main():
    scraper_factory = ScraperFactory()
    transformer_factory = TransformerFactory()
    processor_factory = ProcessorFactory()

    scraper = scraper_factory.get_scraper("the_guardian")
    transformer = transformer_factory.get_transformer("the_guardian")
    processor = processor_factory.get_processor("bigquery")

    # Extração dos dados
    extracted_data = await scraper.extract()

    # Tratamento dos dados
    transformed_data = transformer.transform(extracted_data)

    # Processamento e envio dos dados
    processor.process(transformed_data)

if __name__ == "__main__":
    asyncio.run(main())