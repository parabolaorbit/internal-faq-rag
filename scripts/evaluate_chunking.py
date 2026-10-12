document = """
当社の有給休暇は勤怠管理システムから申請します。
原則として休暇取得日の3営業日前までに上長へ申請してください。

経費精算は経費精算システムから申請します。
当月利用分は翌月5日までに申請する必要があります。

Windowsパスワードを変更する場合は、
Ctrl+Alt+Deleteを押してパスワード変更を選択してください。

在宅勤務を行う場合は、
前営業日までに上長の承認を取得してください。
"""

evaluation_cases = [
    {
        "query": "有給休暇はどこから申請しますか？",
        "expected": "勤怠管理システム",
    },
    {
        "query": "経費精算の締切日はいつですか？",
        "expected": "翌月5日",
    },
    {
        "query": "Windowsパスワードの変更方法は？",
        "expected": "Ctrl+Alt+Delete",
    },
    {
        "query": "在宅勤務には誰の承認が必要ですか？",
        "expected": "上長",
    },
]

from faq_rag.embedding_client import EmbeddingClient
from faq_rag.similarity import cosine_similarity

def retrieve(
        query: str,
        chunks: list[str],
        client: EmbeddingClient,
) -> list[tuple[float, str]]:
    query_vector = client.embed(query)

    results = []

    for chunk in chunks:
        chunk_vector = client.embed(chunk)

        score = cosine_similarity(
            query_vector,
            chunk_vector,
        )
        results.append((score, chunk))

    return sorted(
        results,
        key=lambda item: item[0],
        reverse=True,
    )

def evaluate_recall_at_k(
        cases: list[dict[str, str]],
        chunks: list[str],
        client: EmbeddingClient,
        k: int,
) -> float:
    hits = 0

    for case in cases:
        results = retrieve(
            case["query"],
            chunks,
            client,
        )

        top_chunks = [
            chunk
            for _, chunk in results[:k]
        ]

        if any(
            case["expected"] in chunk
            for chunk in top_chunks
        ):
            hits += 1

    return hits / len(cases)

from faq_rag.chunker import (
    TextChunker,
    ParagraphChunker,
)

strategies = {
    "fixed_40_0": TextChunker(40, 0),
    "fixed_80_0": TextChunker(80, 0),
    "fixed_80_20": TextChunker(80, 20),
    "fixed_160_20": TextChunker(160, 20),
    "paragraph": ParagraphChunker(),
}

client = EmbeddingClient()

for name, chunker in strategies.items():
    chunks = chunker.split(document)

    recall_1 = evaluate_recall_at_k(
        evaluation_cases, chunks, client, 1
    )

    recall_3 = evaluate_recall_at_k(
        evaluation_cases, chunks, client, 3
    )

    print(
        f"{name:15s} "
        f"chunks:{len(chunks):2d} "
        f"Recall@1:{recall_1:.2f} "
        f"Recall@3:{recall_3:.2f}"
    )