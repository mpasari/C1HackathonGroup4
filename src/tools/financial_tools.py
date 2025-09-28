# This module provides tools for financial news and intent detection using APIs and LLMs.
import os
import requests
from datetime import datetime
from typing import Tuple

from src.utils.llm_registry import invoke_llm, zero_metrics, LLMCallMetrics
from src.utils.structured_data import build_structured_record

# API keys for Finnhub and Alpha Vantage are loaded from environment variables.
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

_PROMPT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "prompts", "finance_intent_prompt.txt")
)
with open(_PROMPT_PATH, "r", encoding="utf-8") as prompt_file:
    FINANCE_INTENT_PROMPT = prompt_file.read()


def _format_epoch(value):
    try:
        return datetime.utcfromtimestamp(float(value)).isoformat() + "Z"
    except Exception:
        return None


def is_financial_intent(topic: str) -> Tuple[bool, LLMCallMetrics]:
    """Return (decision, metrics) for finance intent detection."""
    prompt = FINANCE_INTENT_PROMPT.format(query=topic)
    try:
        response, metrics = invoke_llm("finance_intent_checker", prompt)
        answer = response.content.strip().lower()
        return answer.startswith("yes"), metrics
    except Exception:
        metrics = zero_metrics("finance_intent_checker")
        finance_keywords = [
            "stock",
            "finance",
            "market",
            "nifty",
            "sensex",
            "nasdaq",
            "dow",
            "bse",
            "nse",
            "share",
            "equity",
            "mutual fund",
            "ipo",
            "earnings",
            "dividend",
            "invest",
            "portfolio",
            "bond",
            "fii",
            "dii",
            "fpi",
            "etf",
            "s&p",
            "nyse",
            "exchange",
            "commodities",
            "forex",
            "currency",
        ]
        topic_lower = topic.lower()
        return any(word in topic_lower for word in finance_keywords), metrics


def get_finnhub_news(symbol: str, from_date: str, to_date: str):
    """
    Fetches company news from Finnhub for a given symbol and date range.
    Returns a list of news item dicts.
    """
    if not FINNHUB_API_KEY:
        return []
    url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from={from_date}&to={to_date}&token={FINNHUB_API_KEY}"
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    return []


def get_alphavantage_news(symbol: str):
    """
    Fetches news sentiment from Alpha Vantage for a given symbol.
    Returns a list of news item dicts.
    """
    if not ALPHAVANTAGE_API_KEY:
        return []
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&apikey={ALPHAVANTAGE_API_KEY}"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        return data.get("feed", [])
    return []


def get_financial_news(topic: str, symbol: str = None):
    """
    Returns combined structured news from Finnhub and Alpha Vantage for a given stock symbol or topic.
    Each item contains published date, title, authors, summary, content, source, and pdf_url.
    """
    import datetime as _dt

    today = _dt.date.today()
    week_ago = today - _dt.timedelta(days=7)
    symbol = symbol or topic.upper()
    finnhub_news = get_finnhub_news(symbol, str(week_ago), str(today))
    alphav_news = get_alphavantage_news(symbol)

    structured_items = []

    for item in finnhub_news or []:
        published = item.get("datetime") or item.get("publishedDate")
        if isinstance(published, (int, float, str)) and str(published).isdigit():
            published_value = _format_epoch(published)
        else:
            published_value = published
        structured_items.append(
            build_structured_record(
                title=item.get("headline"),
                summary=item.get("summary") or item.get("headline"),
                content=item.get("summary") or item.get("headline"),
                source=item.get("url"),
                published_date=published_value,
                authors=[item.get("source")] if item.get("source") else None,
            )
        )

    for item in alphav_news or []:
        published = item.get("time_published")
        summary = item.get("summary") or item.get("title")
        url = item.get("url")
        pdf_url = url if url and url.lower().endswith(".pdf") else None
        structured_items.append(
            build_structured_record(
                title=item.get("title"),
                summary=summary,
                content=summary,
                source=url,
                published_date=published,
                authors=item.get("authors"),
                pdf_url=pdf_url,
            )
        )

    return structured_items
