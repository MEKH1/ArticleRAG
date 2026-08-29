from pydantic import BaseModel, HttpUrl


class ArticleRequest(BaseModel):
    url: HttpUrl