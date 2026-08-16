import csv
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_PATH = PROJECT_ROOT / "logs" / "usage.csv"

class UsageRecord:

    def logging(
        self,
        model,
        prompt_type,
        input_tokens,
        output_tokens,
        latency_ms,
        estimated_cost
    ) -> None:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

        file_is_empty = not LOG_PATH.exists() or LOG_PATH.stat().st_size == 0

        with LOG_PATH.open(
            mode="a",
            newline="",
            encoding="utf-8-sig",
        ) as csv_file:
            writer = csv.writer(csv_file)

            if file_is_empty:
                writer.writerow([
                    "timestamp",
                    "model",
                    "prompt_type",
                    "input_tokens",
                    "output_tokens",
                    "total_tokens",
                    "latency_ms",
                    "estimated_cost",
                ])

            writer.writerow([
                datetime.now().astimezone().isoformat(timespec="seconds"),
                model,
                str(prompt_type),
                input_tokens,
                output_tokens,
                input_tokens + output_tokens,
                round(latency_ms, 2),
                estimated_cost,
            ])