from faq_rag.embedding_client import EmbeddingClient

def main() -> None:
    client = EmbeddingClient()

    text = "有給休暇の申請方法"

    vector = client.embed(text)

    print(f"text: {text}")
    print(f"dimension: {len(vector)}")
    print(f"first 10 values: {vector[:10]}")

if __name__ == "__main__":
    main()