# ArticleRAG

ArticleRAG is an AI powered research assistant that lets you add online articles and ask questions about their content.

Instead of manually reading through long articles, you can provide one or more article URLs and ask questions in natural language. ArticleRAG finds the most relevant information from the articles and uses it to generate an answer based on the provided sources.

## Live Demo

Try ArticleRAG here:

https://chimerical-dango-2bfbf7.netlify.app/

> The application uses a free backend hosting service. If it has been inactive, the first request may take a short time while the server starts.

## What Can You Do?

### Add Articles

Paste the URL of an online article into the application.

ArticleRAG automatically extracts the article content and prepares it for searching.

### Ask Questions

Once articles have been added, ask questions about their content.

For example:

> Why is this technology useful for data centers?

> What are the main findings of this article?

> What problem are the researchers trying to solve?

### Get Source Based Answers

ArticleRAG searches the indexed articles for information relevant to your question and uses those sections to generate an answer.

The relevant sources are displayed with the answer so you can see where the information came from.

### Use Multiple Articles

You can add multiple articles and ask questions across the indexed collection.

Articles can also be removed when they are no longer needed.

## How It Works

ArticleRAG uses Retrieval Augmented Generation (RAG).

```text
Add Article URL
      ↓
Article Content Extraction
      ↓
Content Processing
      ↓
Semantic Search
      ↓
Ask a Question
      ↓
Retrieve Relevant Information
      ↓
AI Generated Answer
      ↓
Sources
```

This approach helps ground the generated answers in the articles you provide rather than relying only on the AI model's existing knowledge.

## Try It

Open the live application:

https://chimerical-dango-2bfbf7.netlify.app/

Add an article URL, wait for it to be processed, and then start asking questions about its content.

## License

This project is licensed under the MIT License.