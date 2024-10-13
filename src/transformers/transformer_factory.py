# src/transformers/transformer_factory.py
from src.transformers.the_guardian_transformer import TheGuardianTransformer

class TransformerFactory:
    def get_transformer(self, source_name):
        if source_name == "the_guardian":
            return TheGuardianTransformer()
        raise ValueError(f"Transformer for {source_name} not found")
