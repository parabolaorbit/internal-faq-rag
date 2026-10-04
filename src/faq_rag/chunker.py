class TextChunker:
    def __init__(
            self,
            chunk_size: int = 100,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than 0"
            )
        self.chunk_size = chunk_size

    def split(self, text: str) -> list[str]:
        normalized_text = text.strip()

        if not normalized_text:
            return []

        return [
            normalized_text[
                i : i + self.chunk_size
            ]
            for i in range(
                0,
                len(normalized_text),
                self.chunk_size,
            )
        ]