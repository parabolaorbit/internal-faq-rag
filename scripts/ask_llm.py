import logging
import sys

from faq_rag.llm_client import ClaudeClient

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s "
            "%(levelname)s "
            "%(name)s "
            "%(message)s"
        ),
    )

def main() -> int:
    configure_logging()

    question = input("質問を入力してください: ").strip()

    if not question:
        print("質問が入力されていません。")
        return 1

    try:
        client = ClaudeClient()
        result = client.answer_question(question)

    except ValueError as exc:
        print(f"入力エラー: {exc}")
        return 1

    except Exception:
        logging.exception(
            "Claude APIの呼び出しに失敗しました。"
        )
        return 1

    print("\n--- 回答 ---")
    print(result.answer)

    print("\n--- API情報 ---")
    print(f"model           : {result.model}")
    print(f"input_tokens    : {result.input_tokens}")
    print(f"output_tokens   : {result.output_tokens}")
    print(f"total_tokens    : {result.total_tokens}")
    print(f"latency_ms      : {result.latency_ms}")
    return 0

if __name__ == "__main__":
    sys.exit(main())