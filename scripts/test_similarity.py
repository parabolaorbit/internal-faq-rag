from faq_rag.embedding_client import EmbeddingClient
from faq_rag.similarity import cosine_similarity

def main() -> None:
    client = EmbeddingClient()

    text_a = (
        "有給休暇の申請方法を教えてください"
    )

    text_b = (
        "休暇を取得するための"
        "手続きを知りたいです"
    )

    text_c = (
        "Windowsのパスワードを"
        "変更する方法を教えてください"
    )

    vector_a = client.embed(text_a)
    vector_b = client.embed(text_b)
    vector_c = client.embed(text_c)

    similarity_ab = cosine_similarity(
        vector_a,
        vector_b,
    )

    similarity_ac = cosine_similarity(
        vector_a,
        vector_c,
    )

    print(
        f"A vs B: {similarity_ab:.4f}"
    )

    print(
        f"A vs C: {similarity_ac:.4f}"
    )

if __name__ == "__main__":
    main()
