import logging
import sys

from faq_rag.llm_client import ClaudeClient

def main() -> int:
    question = input(
        "質問を入力してください: "
    ).strip()

    if not question:
        print("質問が入力されていません。")
        return 1

    try:
        client = ClaudeClient()
        result = client.answer_question_structured(
            question
        )
    except Exception:
        logging.exception(
            "Structured Outputの取得に失敗しました。"
        )
        return 1

    print("\n--- Structured Answer ---")
    print(f"answer: {result.answer}")
    print(
        f"confidence: {result.confidence}"
    )
    print(
        "needs_more_information: "
        f"{result.needs_more_information}"
    )
    return 0

if __name__ == "__main__":
    sys.exit(main())