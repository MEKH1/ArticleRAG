import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(
    question: str,
    retrieved_chunks: list[dict]
) -> str:

    context_parts = []

    for chunk in retrieved_chunks:
        context_parts.append(
            f"""
Title: {chunk.get("title")}
Source: {chunk.get("url")}

Content:
{chunk.get("text")}
"""
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a research assistant.

Answer the user's question using only the provided context.

If the answer cannot be found in the context, say:
"I could not find this information in the indexed articles."

Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text