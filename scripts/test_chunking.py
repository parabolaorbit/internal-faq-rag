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

from faq_rag.chunker import TextChunker

chunker = TextChunker(
    chunk_size=80
)

chunks = chunker.split(document)

for index, chunk in enumerate(
    chunks,
    start=1,
):
    print(
        f"\n--- Chunk {index} ---"
    )
    print(chunk)

from faq_rag.embedding_client import (
    EmbeddingClient,
)

client = EmbeddingClient()

chunk_vectors = [
    client.embed(chunk)
    for chunk in chunks
]

query = "経費精算の締切日はいつですか？"

query_vector = client.embed(query)

from faq_rag.similarity import (
    cosine_similarity,
)

results = []

for chunk, vector in zip(
    chunks,
    chunk_vectors,
):
    score = cosine_similarity(
        query_vector,
        vector,
    )

    results.append(
        (score, chunk)
    )

for score, chunk in results:
    print(
        f"\n--- Score: {score:.4f} ---"
    )
    print(chunk)

whole_vector = client.embed(
    document
)


whole_score = cosine_similarity(
    query_vector,
    whole_vector,
)

print(
    f"whole document: {whole_score:.4f}"
)
