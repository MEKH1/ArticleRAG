const API_URL = import.meta.env.VITE_API_URL;

export async function getArticles() {
  const response = await fetch(
    `${API_URL}/articles`
  );

  if (!response.ok) {
    throw new Error("Could not load articles");
  }

  return response.json();
}


export async function addArticle(url) {
  const response = await fetch(
    `${API_URL}/articles`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url: url,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Could not add article"
    );
  }

  return data;
}


export async function askQuestion(question) {
  const response = await fetch(
    `${API_URL}/chat`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: question,
        k: 3,
      }),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Could not generate answer"
    );
  }

  return data;
}


export async function deleteArticle(articleId) {
  const response = await fetch(
    `${API_URL}/articles/${articleId}`,
    {
      method: "DELETE",
    }
  );

  if (!response.ok) {
    throw new Error(
      "Could not delete article"
    );
  }

  return response.json();
}