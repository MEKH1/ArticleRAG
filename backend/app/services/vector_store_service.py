import json
import os

import faiss
faiss.omp_set_num_threads(1)
import numpy as np


class VectorStore:
    def __init__(
        self,
        dimension: int,
        index_path: str = "data/faiss.index",
        metadata_path: str = "data/metadata.json"
    ):
        self.dimension = dimension
        self.index_path = index_path
        self.metadata_path = metadata_path

        os.makedirs("data", exist_ok=True)

        self.metadata = {}
        self.next_vector_id = 0

        self._load()


    def _create_index(self):
        base_index = faiss.IndexFlatIP(self.dimension)
        return faiss.IndexIDMap2(base_index)


    def _load(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(
                self.index_path
            )
        else:
            self.index = self._create_index()

        if os.path.exists(self.metadata_path):
            with open(
                self.metadata_path,
                "r",
                encoding="utf-8"
            ) as file:
                saved_metadata = json.load(file)

            self.metadata = {
                int(key): value
                for key, value
                in saved_metadata.items()
            }

            if self.metadata:
                self.next_vector_id = (
                    max(self.metadata.keys()) + 1
                )
        else:
            self.metadata = {}


    def _save(self):
        faiss.write_index(
            self.index,
            self.index_path
        )

        with open(
            self.metadata_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                self.metadata,
                file,
                ensure_ascii=False,
                indent=2
            )


    def add_embeddings(
        self,
        embeddings: list[list[float]],
        chunks: list[dict],
        article: dict,
        article_id: str
    ):
        vectors = np.array(
            embeddings,
            dtype="float32"
        )

        vector_ids = np.arange(
            self.next_vector_id,
            self.next_vector_id + len(vectors),
            dtype="int64"
        )

        self.index.add_with_ids(
            vectors,
            vector_ids
        )

        for vector_id, chunk in zip(
            vector_ids,
            chunks
        ):
            self.metadata[int(vector_id)] = {
                "article_id": article_id,
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "title": article.get("title"),
                "url": article.get("url"),
                "author": article.get("author"),
                "date": article.get("date")
            }

        self.next_vector_id += len(vectors)

        self._save()


    def search(
        self,
        query_embedding: list[float],
        k: int = 3
    ) -> list[dict]:

        if self.index.ntotal == 0:
            return []

        query_vector = np.array(
            [query_embedding],
            dtype="float32"
        )

        scores, ids = self.index.search(
            query_vector,
            min(k, self.index.ntotal)
        )

        results = []

        for score, vector_id in zip(
            scores[0],
            ids[0]
        ):
            if vector_id == -1:
                continue

            vector_id = int(vector_id)

            if vector_id not in self.metadata:
                continue

            item = self.metadata[
                vector_id
            ].copy()

            item["score"] = float(score)

            results.append(item)

        return results


    def url_exists(
        self,
        url: str
    ) -> bool:

        return any(
            item.get("url") == url
            for item in self.metadata.values()
        )


    def list_articles(self) -> list[dict]:

        articles = {}

        for item in self.metadata.values():

            article_id = item["article_id"]

            if article_id not in articles:
                articles[article_id] = {
                    "article_id": article_id,
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "author": item.get("author"),
                    "date": item.get("date"),
                    "chunk_count": 0
                }

            articles[
                article_id
            ]["chunk_count"] += 1

        return list(
            articles.values()
        )


    def delete_article(
        self,
        article_id: str
    ) -> bool:

        vector_ids = [
            vector_id
            for vector_id, item
            in self.metadata.items()
            if item.get("article_id")
            == article_id
        ]

        if not vector_ids:
            return False

        ids = np.array(
            vector_ids,
            dtype="int64"
        )

        self.index.remove_ids(ids)

        for vector_id in vector_ids:
            self.metadata.pop(
                vector_id,
                None
            )

        self._save()

        return True