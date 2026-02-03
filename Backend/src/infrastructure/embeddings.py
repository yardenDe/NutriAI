import numpy as np

class Embeddings:
    def __init__(self, model):
        self.model = model

    def to_embedded(self, symptoms: list[str]) -> list[float]:
            query_text = " ".join(symptoms)
            embedding: np.ndarray = self.model.encode(query_text)
            return embedding.tolist()

