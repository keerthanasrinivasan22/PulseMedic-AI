import ollama

def summarize_articles(articles):
    if not articles:
        return "No news articles found today."

    joined = "\n\n".join(
        f"Title: {a['title']}\nSummary: {a['summary']}" for a in articles
    )

    prompt = f"""
    Summarize the following medical AI news into 3–4 bullet points:

    {joined}
    """

    response = ollama.generate(model="llama3.2", prompt=prompt)
    return response["response"]
