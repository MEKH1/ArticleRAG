import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.models import ArticleRequest

from app.services.article_service import (
    extract_article
)

from app.services.chunking_service import (
    chunk_text
)

from app.services.embedding_service import (
    embed_chunks,
    embed_question
)

from app.services.vector_store_service import (
    VectorStore
)

from app.services.rag_service import (
    generate_answer
)


app = FastAPI(
    title="Article RAG API",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

vector_store = VectorStore(dimension=768)


class SearchRequest(BaseModel):
    question: str
    k: int = 3


class ChatRequest(BaseModel):
    question: str
    k: int = 3


@app.get("/")
def root():
    return {
        "message": "Article RAG API is running"
    }


@app.post("/articles")
def add_article(
    request: ArticleRequest
):
    try:
        url = str(request.url)

        if vector_store.url_exists(url):
            raise HTTPException(
                status_code=409,
                detail=(
                    "This article has "
                    "already been indexed."
                )
            )

        article = extract_article(
            url
        )

        chunks = chunk_text(
            article["text"],
            chunk_size=150,
            overlap=30
        )

        embeddings = embed_chunks(
            chunks
        )

        article_id = str(
            uuid.uuid4()
        )

        vector_store.add_embeddings(
            embeddings=embeddings,
            chunks=chunks,
            article=article,
            article_id=article_id
        )

        return {
            "success": True,
            "article_id": article_id,
            "title": article["title"],
            "url": article["url"],
            "chunk_count": len(chunks)
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )


@app.get("/articles")
def get_articles():

    articles = vector_store.list_articles()

    return {
        "count": len(articles),
        "articles": articles
    }


@app.delete(
    "/articles/{article_id}"
)
def delete_article(
    article_id: str
):

    deleted = (
        vector_store.delete_article(
            article_id
        )
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Article not found."
        )

    return {
        "success": True,
        "message": (
            "Article deleted successfully."
        )
    }


@app.post("/search")
def search_articles(
    request: SearchRequest
):
    try:
        question_embedding = (
            embed_question(
                request.question
            )
        )

        results = vector_store.search(
            query_embedding=
                question_embedding,
            k=request.k
        )

        return {
            "question": request.question,
            "results": results
        }

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )


@app.post("/chat")
def chat(
    request: ChatRequest
):
    try:
        question_embedding = (
            embed_question(
                request.question
            )
        )

        results = vector_store.search(
            query_embedding=
                question_embedding,
            k=request.k
        )

        if not results:
            return {
                "question":
                    request.question,
                "answer":
                    "No articles have been indexed yet.",
                "sources": []
            }

        answer = generate_answer(
            question=request.question,
            retrieved_chunks=results
        )

        sources = [
            {
                "article_id":
                    result["article_id"],
                "title":
                    result["title"],
                "url":
                    result["url"],
                "score":
                    result["score"]
            }
            for result in results
        ]

        return {
            "question": request.question,
            "answer": answer,
            "sources": sources
        }

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )