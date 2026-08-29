import requests
import trafilatura


def extract_article(url: str) -> dict:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36"
        )
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()

    html = response.text

    text = trafilatura.extract(
        html,
        include_comments=False,
        include_tables=False
    )

    if not text:
        raise ValueError("Could not extract article content")

    metadata = trafilatura.extract_metadata(html)

    title = None
    author = None
    date = None

    if metadata:
        title = metadata.title
        author = metadata.author
        date = metadata.date

    return {
        "url": url,
        "title": title,
        "author": author,
        "date": date,
        "text": text
    }