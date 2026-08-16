from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


class UsageRecord:

    def logging(
        self,
        model,
        prompt_type,
        input_tokens,
        output_tokens,
        latency_ms,
        estimated_cost
    ):
        logger.info(
                    "llm_request_completed "
                    "prompt_type=%s"
                    "model=%s "
                    "input_tokens=%d "
                    "output_tokens=%d "
                    "total_tokens=%d "
                    "latency_ms=%.2f",
                    "estimated_cost",
                    model,
                    prompt_type,
                    input_tokens,
                    output_tokens,
                    input_tokens + output_tokens,
                    latency_ms,
                    estimated_cost
                )