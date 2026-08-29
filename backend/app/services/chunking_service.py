import re


def split_into_sentences(text: str) -> list[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> list[dict]:

    sentences = split_into_sentences(text)

    chunks = []
    current_chunk = []
    current_word_count = 0

    for sentence in sentences:
        sentence_words = sentence.split()
        sentence_length = len(sentence_words)

        if current_word_count + sentence_length <= chunk_size:
            current_chunk.append(sentence)
            current_word_count += sentence_length

        else:
            if current_chunk:
                chunk_text_value = " ".join(current_chunk)

                chunks.append({
                    "chunk_id": len(chunks),
                    "text": chunk_text_value,
                    "word_count": len(chunk_text_value.split())
                })

            overlap_words = []

            if chunks and overlap > 0:
                previous_words = chunks[-1]["text"].split()
                overlap_words = previous_words[-overlap:]

            current_chunk = []

            if overlap_words:
                current_chunk.append(" ".join(overlap_words))

            current_chunk.append(sentence)

            current_word_count = (
                len(overlap_words) + sentence_length
            )

    if current_chunk:
        chunk_text_value = " ".join(current_chunk)

        chunks.append({
            "chunk_id": len(chunks),
            "text": chunk_text_value,
            "word_count": len(chunk_text_value.split())
        })

    return chunks