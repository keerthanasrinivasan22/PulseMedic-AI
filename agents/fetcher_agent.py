# agents/fetcher_agent.py

import datetime as dt
from typing import List, Dict, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
import feedparser

# ---------- CONFIG ----------

USER_AGENT = (
    "PulseMedic-AI/0.1 (educational project; contact: local-user) "
    "Mozilla/5.0"
)

# Each source can optionally have an rss_url.
# For now most rss_url values are None; if you later discover the
# real RSS feeds, just fill them in and RSS will be used automatically.
NEWS_SOURCES = [
    {
        "name": "AI in Healthcare",
        "url": "https://www.aiin.healthcare",
        "rss_url": None,  # e.g. "https://www.aiin.healthcare/rss" if available
    },
    {
        "name": "AI in Healthcare – Newsletters",
        "url": "https://aiin.healthcare/newsletters",
        "rss_url": None,
    },
    {
        "name": "NEJM AI",
        "url": "https://ai.nejm.org",
        "rss_url": None,  # fill real RSS here if you find it
    },
    {
        "name": "AMA Health Care AI",
        "url": "https://www.ama-assn.org/topics/health-care-ai",
        "rss_url": None,
    },
    {
        "name": "STAT Health Tech (AI & Health Tech)",
        "url": "https://www.statnews.com/category/health-tech",
        "rss_url": None,
    },
    {
        "name": "Modern Healthcare – Digital Health Intelligence",
        "url": "https://www.modernhealthcare.com/newsletters/digital-health-intelligence",
        "rss_url": None,
    },
    {
        "name": "Healthcare Dive – IT Weekly",
        "url": "https://www.healthcaredive.com/newsletters/it-weekly",
        "rss_url": None,
    },
    {
        "name": "mHealthIntelligence",
        "url": "https://mhealthintelligence.com/resources/newsletters",
        "rss_url": None,
    },
    {
        "name": "Digital Health Wire",
        "url": "https://digitalhealthwire.com",
        "rss_url": None,
    },
    {
        "name": "Axios AI+",
        "url": "https://www.axios.com/newsletters/axios-ai",
        "rss_url": None,
    },
]


# ---------- CORE HELPERS ----------

def _http_get(url: str) -> Optional[str]:
    """Safe HTTP GET with basic headers & timeouts."""
    try:
        resp = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": USER_AGENT},
        )
        if resp.status_code == 200:
            return resp.text
    except Exception as e:
        print(f"[fetcher] Error fetching URL {url}: {e}")
    return None


def _is_recent(published: Optional[dt.datetime], days: int = 2) -> bool:
    """Check if a datetime is within the last `days` days."""
    if not published:
        return True  # if we don't know, don't filter it out
    now = dt.datetime.utcnow()
    return (now - published) <= dt.timedelta(days=days)


# ---------- RSS FETCHING (Option C: path A) ----------

def _fetch_from_rss(rss_url: str, source_name: str) -> List[Dict]:
    """Fetch articles from an RSS feed."""
    print(f"[fetcher] Trying RSS for {source_name}: {rss_url}")
    articles: List[Dict] = []

    try:
        feed = feedparser.parse(rss_url)
    except Exception as e:
        print(f"[fetcher] RSS error for {source_name}: {e}")
        return articles

    for entry in feed.entries:
        title = getattr(entry, "title", "").strip()
        link = getattr(entry, "link", "").strip()

        if not title or not link:
            continue

        # Try to parse published date if available
        published_dt = None
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            published_dt = dt.datetime(*entry.published_parsed[:6])

        if not _is_recent(published_dt, days=2):
            continue

        summary_text = getattr(entry, "summary", "") or getattr(entry, "description", "")
        summary_text = BeautifulSoup(summary_text, "html.parser").get_text(" ", strip=True)

        articles.append(
            {
                "title": title,
                "summary": summary_text,
                "link": link,
                "source": source_name,
            }
        )

    return articles


# ---------- HTML SCRAPING (Option C: path B / fallback) ----------

def _extract_articles_from_html(html: str, base_url: str, source_name: str) -> List[Dict]:
    """
    Very generic HTML extraction:
    - Prefer <article> tags
    - Fallback to <a> tags inside main / section
    - Filter links that mention AI / artificial intelligence / machine learning
    """
    soup = BeautifulSoup(html, "html.parser")
    articles: List[Dict] = []

    # 1. Try <article> tags
    article_tags = soup.find_all("article")
    link_candidates = []

    if article_tags:
        for art in article_tags:
            a = art.find("a", href=True)
            if not a:
                continue
            link_candidates.append(a)
    else:
        # 2. Fallback: look for <a> inside <main>, <section>, etc.
        main = soup.find("main") or soup.find("body")
        if main:
            for a in main.find_all("a", href=True):
                link_candidates.append(a)

    seen = set()
    for a in link_candidates:
        href = a.get("href")
        text = a.get_text(" ", strip=True)
        if not href or not text:
            continue

        # Deduplicate by text
        if text in seen:
            continue
        seen.add(text)

        # Basic AI / healthcare relevance filter
        t = text.lower()
        if not (
            "ai" in t
            or "artificial intelligence" in t
            or "machine learning" in t
            or "data" in t
        ):
            # If you want, you can make this stricter or looser
            continue

        full_link = urljoin(base_url, href)
        articles.append(
            {
                "title": text,
                "summary": "",  # summarizer will fill this context-wide
                "link": full_link,
                "source": source_name,
            }
        )

    return articles


def _fetch_from_html_page(url: str, source_name: str) -> List[Dict]:
    """Fetch articles from a normal HTML page."""
    print(f"[fetcher] Scraping HTML for {source_name}: {url}")
    html = _http_get(url)
    if not html:
        return []
    return _extract_articles_from_html(html, url, source_name)


# ---------- PUBLIC FUNCTION USED BY main.py ----------

def fetch_health_ai_news(max_items: int = 10) -> List[Dict]:
    """
    Fetch AI-in-healthcare news from curated sources.

    Option C behavior:
    - For each source:
        1. Try RSS (if rss_url is configured)
        2. If RSS unavailable or empty, scrape HTML
    - Stop once `max_items` unique articles have been collected.
    """
    collected: List[Dict] = []
    seen_titles = set()

    for src in NEWS_SOURCES:
        if len(collected) >= max_items:
            break

        name = src["name"]
        url = src["url"]
        rss_url = src.get("rss_url")

        articles: List[Dict] = []

        # 1. Try RSS if configured
        if rss_url:
            try:
                articles = _fetch_from_rss(rss_url, name)
            except Exception as e:
                print(f"[fetcher] Error using RSS for {name}: {e}")
                articles = []

        # 2. Fallback to HTML scraping
        if not articles:
            try:
                articles = _fetch_from_html_page(url, name)
            except Exception as e:
                print(f"[fetcher] Error scraping HTML for {name}: {e}")
                articles = []

        # 3. Add to global list with deduplication
        for art in articles:
            title = art.get("title", "").strip()
            if not title or title in seen_titles:
                continue

            collected.append(art)
            seen_titles.add(title)

            if len(collected) >= max_items:
                break

    print(f"[fetcher] Total articles collected: {len(collected)}")
    return collected
