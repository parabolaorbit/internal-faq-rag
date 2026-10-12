class TextChunker:
    def __init__(
            self,
            chunk_size: int = 100,
            chunk_overlap: int = 0,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than 0"
            )

        if chunk_overlap < 0:
            raise ValueError(
                "chunk_overlap must be greater than or equal to 0"
            )

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be less than chunk_size"
            )
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(
            self, 
            text: str
        ) -> list[str]:
        normalized_text = text.strip()

        if not normalized_text:
            return []

        step = (
            self.chunk_size
            - self.chunk_overlap
        )

        return [
            normalized_text[
                i : i + self.chunk_size
            ]
            for i in range(
                0,
                len(normalized_text),
                step,
            )
        ]

class ParagraphChunker:
    def split(self, text: str) -> list[str]:
        return [
            paragraph.strip()
            for paragraph in text.split("\n\n")
            if paragraph.strip()
        ]
   