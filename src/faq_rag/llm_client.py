from dataclasses import dataclass
from time import perf_counter
import json
from pydantic import ValidationError

from anthropic import Anthropic

from faq_rag.config import Settings, get_settings
from faq_rag.prompt_builder import PromptBuilder
from faq_rag.prompt_types import PromptType
from faq_rag.schemas import FAQAnswer
from faq_rag.tool_registry import TOOL_DEFINITIONS, TOOL_FUNCTIONS
from faq_rag.cost_calculator import Pricing
from faq_rag.usage_logger import UsageRecord

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

    def answer_question(self, question: str, prompt_type: PromptType) -> LLMAnswer:
        # Question
        normalized_question = question.strip()

        if not normalized_question:
            raise ValueError("Question must not be empty")

        builder = PromptBuilder()
        start_at = perf_counter()
        system_prompt = builder.build_system_prompt(prompt_type=prompt_type)

        # Tool Use
        first_response = self.client.messages.create(
            model=self.settings.anthropic_model,
            max_tokens=1024,
            system=system_prompt,
            tools=TOOL_DEFINITIONS,
            tool_choice={"type": "auto", "disable_parallel_tool_use": True},
            messages=[
                {
                    "role": "user",
                    "content": normalized_question,
                }
            ],
        )

        tool_use = next(
            (block for block in first_response.content if block.type == "tool_use"),
            None,
        )

        total_input_tokens = first_response.usage.input_tokens
        total_output_tokens = first_response.usage.output_tokens

        if tool_use is None:
            response = first_response
        else:
            print(f"Tool used: {tool_use.name}, Input: {tool_use.input}, ID: {tool_use.id}")

            tool_output = TOOL_FUNCTIONS[tool_use.name](**tool_use.input) if tool_use else None

            # Claude
            response = self.client.messages.create(
                model=self.settings.anthropic_model,
                max_tokens=1024,
                system=system_prompt,
                tools=TOOL_DEFINITIONS,
                messages=[
                    {
                        "role": "user",
                        "content": normalized_question,
                    },
                    {
                        "role": "assistant",
                        "content": first_response.content,
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_use.id,
                                "content": str(tool_output),
                            }
                        ]
                    }
                ],
            )

            total_input_tokens += response.usage.input_tokens
            total_output_tokens += response.usage.output_tokens

        latency_ms = (perf_counter() - start_at) * 1000

        answer = self._extract_text(response.content)

        estimated_cost = Pricing().estimate_cost(input_tokens=total_input_tokens, output_tokens=total_output_tokens)
        print(f"estimated_cost is {estimated_cost}")

        # result
        result = LLMAnswer(
            answer=answer,
            model=response.model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            latency_ms=round(latency_ms, 2),
        )

        UsageRecord().logging(
            model=result.model,
            prompt_type=system_prompt,
            input_tokens=result.input_tokens,
            output_tokens=result.output_tokens,
            latency_ms=result.latency_ms,
            estimated_cost=estimated_cost
        )
        return result

    def answer_question_structured(
            self,
            question: str,
    ) -> FAQAnswer:
        result = self.answer_question(
            question=question,
            prompt_type=PromptType.STRUCTURED_FAQ
        )

        try:
            answer = result.answer.strip()
            if answer.startswith("```json") and answer.endswith("```"):
                answer = answer[len("```json"):-len("```")].strip()
            elif answer.startswith("```") and answer.endswith("```"):
                answer = answer[len("```"):-len("```")].strip()
            payload = json.loads(answer)

            return FAQAnswer.model_validate(payload)
        except json.JSONDecodeError as exc:
            print(f"Invalid JSON returned by Claude: {answer}")
            raise ValueError(
                "Claude returned invalid JSON"
            ) from exc
        except ValidationError as exc:
            print(f"Invalid structured output returned by Claude: {answer}")
            raise ValueError(
                "Claude returned invalid structured output"
            ) from exc

    @staticmethod
    def _extract_text(content_blocks) -> str:
        texts = [
            block.text
            for block in content_blocks
            if getattr(block, "type", None) == "text"
        ]

        return "\n".join(texts)