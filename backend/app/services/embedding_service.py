from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts: list[str]) -> list[list[float]]:
    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    return embeddings.tolist()


def embed_chunks(chunks: list[dict]) -> list[list[float]]:
    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    return embed_texts(texts)


def embed_question(question: str) -> list[float]:
    embedding = model.encode(
        question,
        normalize_embeddings=True
    )

    return embedding.tolist()