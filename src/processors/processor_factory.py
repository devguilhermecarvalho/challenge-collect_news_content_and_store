# src/processors/processor_factory.py

from src.processors.bigquery_processor import BigQueryProcessor
import yaml

class ProcessorFactory:
    def __init__(self):
        self.config = self.load_config()

    def load_config(self):
        with open('./src/config/bigquery_config.yaml', 'r') as file:
            return yaml.safe_load(file)

    def get_processor(self, destination_name):
        if destination_name == "bigquery":
            return BigQueryProcessor(self.config)
        raise ValueError(f"Processor for {destination_name} not found")