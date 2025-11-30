# app/main.py

import os
import sys
import streamlit as st

# -------------------------------------------------------------------
# Make sure Python can see the project root so "agents" imports work
# -------------------------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from agents.fetcher_agent import fetch_health_ai_news
from agents.summarizer_agent import summarize_articles

# -------------------------------------------------------------------
# Streamlit page config
# -------------------------------------------------------------------
st.set_page_config(page_title="PulseMedic-AI", page_icon="🩺")

st.title("🩺 PulseMedic-AI")
st.subheader("Daily Medical AI News Summary • Powered by Free Local AI")

st.markdown(
    """
This dashboard fetches **AI-in-healthcare news** from a curated set of professional
sources and summarizes the key updates using a **local Llama 3.2 model (via Ollama)**.
"""
)

# Let user choose how many articles to fetch (from your curated domains)
max_items = st.slider("Maximum articles to fetch", min_value=3, max_value=15, value=8, step=1)

# -------------------------------------------------------------------
# Main button
# -------------------------------------------------------------------
if st.button("Fetch & Summarize Today's Updates"):
    # 1) Fetch articles
    with st.spinner("Fetching latest healthcare AI news from curated sources..."):
        articles = fetch_health_ai_news(max_items=max_items)

    if not articles:
        st.warning(
            "No news articles found today from your selected healthcare AI sources. "
            "Try again later, or increase the date range in the fetcher if needed."
        )
    else:
        # 2) Summarize with Llama via Ollama
        with st.spinner("Generating summary using Llama3.2 (local Ollama)..."):
            summary = summarize_articles(articles)

        st.success("Summary Ready!")
        st.markdown(summary)

        # 3) Show full article list
        st.divider()
        st.subheader("Full Articles")

        for article in articles:
            title = article.get("title", "(no title)")
            snippet = article.get("summary", "")
            link = article.get("link", "")
            source = article.get("source") or ""

            # Card-like display
            st.markdown(f"### {title}")
            if source:
                st.caption(f"Source: {source}")

            if snippet:
                st.write(snippet)

            if link:
                st.markdown(f"[Read more]({link})")

            st.markdown("---")
