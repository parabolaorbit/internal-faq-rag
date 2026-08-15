from typing import Literal

from pydantic import BaseModel, Field

class FAQAnswer(BaseModel):
    answer: str = Field(
        description="ユーザー質問への回答"
    )

    confidence: Literal[
        "high",
        "medium",
        "low",
    ] = Field(
        description="回答の信頼度"
    )

    needs_more_information: bool = Field(
        description=(
            "回答するために追加情報が必要か"
        )
    )