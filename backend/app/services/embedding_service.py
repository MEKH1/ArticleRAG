import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIMENSION = 768


def embed_texts(texts: list[str]) -> list[list[float]]:
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSION
        )
    )

    return [
        embedding.values
        for embedding in result.embeddings
    ]


def embed_chunks(chunks: list[dict]) -> list[list[float]]:
    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    return embed_texts(texts)


def embed_question(question: str) -> list[float]:
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=question,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSION
        )
    )

    return result.embeddings[0].values