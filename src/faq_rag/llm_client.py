import logging
from dataclasses import dataclass
from time import perf_counter

from anthropic import Anthropic

from faq_rag.config import Settings, get_settings

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class LLMAnswer:
    answer: str
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    latency_ms: float

class ClaudeClient:
    """Claude Messages API client."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

        self.client = Anthropic(
            api_key=self.settings.anthropic_api_key.get_secret_value()
        )

    def answer_question(self, question: str) -> LLMAnswer:
        normalized_question = question.strip()

        if not normalized_question:
            raise ValueError("Question must not be empty")

        start_at = perf_counter()

        response = self.client.messages.create(
            model=self.settings.anthropic_model,
            max_tokens=1024,
            system=(
                "あなたは社内FAQの回答アシスタントです。"
                "質問に対して簡潔で分かりやすい日本語で回答してください。"
                "与えられていない社内情報を推測しないでください。"
            ),
            messages=[
                {
                    "role": "user",
                    "content": normalized_question,
                }
            ],
        )

        latency_ms = (perf_counter() - start_at) * 1000

        answer = self._extract_text(response.content)

        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

        result = LLMAnswer(
            answer=answer,
            model=response.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            latency_ms=round(latency_ms, 2),
        )

        logger.info(
            "llm_request_completed "
            "model=%s "
            "input_tokens=%d "
            "output_tokens=%d "
            "total_tokens=%d "
            "latency_ms=%.2f",
            result.model,
            result.input_tokens,
            result.output_tokens,
            result.total_tokens,
            result.latency_ms,
        )
        return result

    @staticmethod
    def _extract_text(content_blocks) -> str:
        texts = [
            block.text
            for block in content_blocks
            if getattr(block, "type", None) == "text"
        ]

        return "\n".join(texts)