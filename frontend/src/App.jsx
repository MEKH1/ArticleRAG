import { useEffect, useState } from "react";
import {
  addArticle,
  askQuestion,
  deleteArticle,
  getArticles,
} from "./api";

import "./App.css";


function App() {
  const [articles, setArticles] = useState([]);
  const [url, setUrl] = useState("");
  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([]);

  const [loadingArticle, setLoadingArticle] =
    useState(false);

  const [loadingAnswer, setLoadingAnswer] =
    useState(false);

  const [error, setError] = useState("");


  async function loadArticles() {
    try {
      const data = await getArticles();
      setArticles(data.articles);
    } catch (err) {
      setError(err.message);
    }
  }


  useEffect(() => {
    loadArticles();
  }, []);


  async function handleAddArticle(event) {
    event.preventDefault();

    if (!url.trim()) {
      return;
    }

    setLoadingArticle(true);
    setError("");

    try {
      await addArticle(url);

      setUrl("");

      await loadArticles();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingArticle(false);
    }
  }


  async function handleDelete(articleId) {
    setError("");

    try {
      await deleteArticle(articleId);

      await loadArticles();
    } catch (err) {
      setError(err.message);
    }
  }


  async function handleQuestion(event) {
    event.preventDefault();

    const currentQuestion = question.trim();

    if (!currentQuestion) {
      return;
    }

    setQuestion("");
    setError("");

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: currentQuestion,
      },
    ]);

    setLoadingAnswer(true);

    try {
      const data = await askQuestion(
        currentQuestion
      );

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources,
        },
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingAnswer(false);
    }
  }


  function clearChat() {
    setMessages([]);
  }


  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            AI
          </div>

          <div>
            <h1>Article RAG</h1>
            <p>Research assistant</p>
          </div>
        </div>

        <form
          className="article-form"
          onSubmit={handleAddArticle}
        >
          <label>
            Add article
          </label>

          <input
            type="url"
            placeholder="Paste article URL"
            value={url}
            onChange={(event) =>
              setUrl(event.target.value)
            }
          />

          <button
            type="submit"
            disabled={loadingArticle}
          >
            {loadingArticle
              ? "Indexing..."
              : "Add article"}
          </button>
        </form>

        <div className="articles-header">
          <span>
            Indexed articles
          </span>

          <span className="article-count">
            {articles.length}
          </span>
        </div>

        <div className="article-list">
          {articles.length === 0 ? (
            <div className="empty-articles">
              <p>
                No articles yet.
              </p>

              <span>
                Add an article to begin.
              </span>
            </div>
          ) : (
            articles.map((article) => (
              <article
                className="article-card"
                key={article.article_id}
              >
                <div className="article-info">
                  <a
                    href={article.url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    {article.title}
                  </a>

                  <span>
                    {article.author ||
                      "Unknown author"}
                  </span>

                  {article.date && (
                    <span>
                      {article.date}
                    </span>
                  )}

                  <span>
                    {article.chunk_count} chunks
                  </span>
                </div>

                <button
                  className="delete-button"
                  onClick={() =>
                    handleDelete(
                      article.article_id
                    )
                  }
                >
                  ×
                </button>
              </article>
            ))
          )}
        </div>
      </aside>

      <main className="chat-section">
        <header className="chat-header">
          <div>
            <h2>
              Ask your articles
            </h2>

            <p>
              Answers are generated from
              your indexed sources.
            </p>
          </div>

          {messages.length > 0 && (
            <button
              className="clear-button"
              onClick={clearChat}
            >
              Clear chat
            </button>
          )}
        </header>

        <div className="chat-container">
          {messages.length === 0 ? (
            <div className="welcome">
              <div className="welcome-icon">
                AI
              </div>

              <h2>
                What would you like to know?
              </h2>

              <p>
                Add articles, then ask
                questions about their content.
              </p>

              <div className="examples">
                <div>
                  Summarize the main findings
                </div>

                <div>
                  What problem does this solve?
                </div>

                <div>
                  Compare the indexed articles
                </div>
              </div>
            </div>
          ) : (
            <div className="messages">
              {messages.map(
                (message, index) => (
                  <div
                    key={index}
                    className={`message-row ${
                      message.role
                    }`}
                  >
                    <div
                      className={`message ${
                        message.role
                      }`}
                    >
                      <div className="message-role">
                        {message.role ===
                        "user"
                          ? "You"
                          : "Article AI"}
                      </div>

                      <p>
                        {message.content}
                      </p>

                      {message.sources &&
                        message.sources.length >
                          0 && (
                          <div className="sources">
                            <span className="sources-title">
                              Sources
                            </span>

                            {message.sources.map(
                              (
                                source,
                                sourceIndex
                              ) => (
                                <a
                                  key={
                                    sourceIndex
                                  }
                                  href={
                                    source.url
                                  }
                                  target="_blank"
                                  rel="noreferrer"
                                  className="source-card"
                                >
                                  <span>
                                    {
                                      source.title
                                    }
                                  </span>

                                  {typeof source.score ===
                                    "number" && (
                                    <small>
                                      Similarity{" "}
                                      {source.score.toFixed(
                                        3
                                      )}
                                    </small>
                                  )}
                                </a>
                              )
                            )}
                          </div>
                        )}
                    </div>
                  </div>
                )
              )}

              {loadingAnswer && (
                <div className="message-row assistant">
                  <div className="message assistant loading-message">
                    <div className="message-role">
                      Article AI
                    </div>

                    <div className="typing">
                      <span />
                      <span />
                      <span />
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <form
          className="question-form"
          onSubmit={handleQuestion}
        >
          <input
            type="text"
            placeholder={
              articles.length === 0
                ? "Add an article first..."
                : "Ask a question about your articles..."
            }
            value={question}
            onChange={(event) =>
              setQuestion(
                event.target.value
              )
            }
            disabled={
              loadingAnswer ||
              articles.length === 0
            }
          />

          <button
            type="submit"
            disabled={
              loadingAnswer ||
              articles.length === 0 ||
              !question.trim()
            }
          >
            Send
          </button>
        </form>
      </main>
    </div>
  );
}


export default App;