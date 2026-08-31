from faq_rag.embedding_client import EmbeddingClient
from faq_rag.similarity import cosine_similarity

def main() -> None:
    client = EmbeddingClient()
    query = "休暇を取るにはどうすればいいですか？"
    query_vector = client.embed(query)
    documents = [
        "有給休暇は勤怠システムから申請します。",
        "WindowsパスワードはCtrl+Alt+Deleteから変更できます。",
        "経費精算は経費システムから申請します。",
    ]

    results = []
    for document in documents:
        document_vector = client.embed(document)

        score = cosine_similarity(
            query_vector,
            document_vector,
        )

        results.append(
            (score, document)
        )

    results.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    for score, document in results:
        print(
            f"{score:.4f}: {document}"
        )

if __name__ == "__main__":
    main()
