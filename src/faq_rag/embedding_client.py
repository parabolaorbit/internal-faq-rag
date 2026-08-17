from sentence_transformers import SentenceTransformer

class EmbeddingClient:
    def __init__(
            self,
            model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ) -> None:
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list[float]:
        normalized_text = text.strip()
        if not normalized_text:
            raise ValueError("text must not be empty")

        embedding = self.model.encode(
            normalized_text,
            normalize_embeddings=True,
        )

        return embedding.tolist()