import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

NEWS_SOURCES = [
    "https://www.medicalnewstoday.com/rss",
    "https://www.healthit.gov/newsroom/rss.xml",
    "https://www.sciencedaily.com/rss/health.xml",
    "https://www.fiercehealthcare.com/rss",
    "https://www.fiercebiotech.com/rss",
    "https://www.beckershospitalreview.com/feed",
]
