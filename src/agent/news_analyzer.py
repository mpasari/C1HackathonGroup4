import time
from typing import Any, Dict, List

# This module defines the news analyzer agent, which retrieves and summarizes news articles for a topic.
from src.utils.llm_registry import get_llm
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.graph.state import ResearchState
from src.tools.news_tools import news_api_tool, news_search
from src.utils.structured_data import build_structured_record

# LLM and embeddings are initialized for possible use in summarization or advanced features.
llm = get_llm("research_assistant")
embeddings = HuggingFaceEmbeddings()


def _normalize_results(results: Any, limit: int) -> List[Any]:
    if isinstance(results, list):
        return results[:limit]
    if isinstance(results, str):
        return [results][:limit]
    return []


def _structure_item(item: Any) -> Dict[str, Any]:
    if isinstance(item, dict):
        title = item.get("title") or item.get("name")
        summary = item.get("summary") or item.get("description") or item.get("snippet")
        content = (
            item.get("raw_content")
            or item.get("content")
            or item.get("full_content")
            or item.get("body")
            or item.get("text")
            or summary
            or title
        )
        source = item.get("url") or item.get("link")
        published = item.get("published_at") or item.get("published") or item.get("date")
        authors = item.get("authors") or item.get("author") or item.get("byline")
    else:
        text = str(item)
        title = text[:120]
        summary = text
        content = text
        source = None
        published = None
        authors = None
    return build_structured_record(
        title=title,
        summary=summary,
        content=content,
        source=source,
        published_date=published,
        authors=authors,
    )


def _structure_items(items: List[Any]) -> List[Dict[str, Any]]:
    return [_structure_item(item) for item in items]


def _fetch_results(tool, query: str, limit: int) -> Dict[str, Any]:
    try:
        raw = tool.run(query)
        normalized = _normalize_results(raw, limit)
        return {"items": _structure_items(normalized)}
    except Exception as exc:  # pragma: no cover - defensive
        return {"items": [], "error": str(exc)}


def analyze_news(state: ResearchState) -> dict:
    """
    The news analyzer agent retrieves news articles for the given topic using NewsAPI or DuckDuckGo.
    Returns a dictionary with raw tool outputs and metadata.
    """
    start = time.time()
    topic = state['topic']
    mode = state.get('mode', 'extended')
    num_items = 2 if mode == 'simple' else 10

    if news_api_tool:
        primary_tool = news_api_tool
        primary_name = 'news_api'
        query = topic
    else:
        primary_tool = news_search
        primary_name = 'duckduckgo_news'
        query = f"news {topic}"

    payload = _fetch_results(primary_tool, query, num_items)
    items = payload.get("items", [])
    sources: List[Dict[str, Any]] = [
        {
            "name": primary_name,
            "items": items,
            "metadata": {
                "limit": num_items,
                "item_count": len(items),
                "provider": primary_name,
                **({"error": payload["error"]} if "error" in payload else {}),
            },
        }
    ]

    elapsed = time.time() - start
    return {
        "news_results": {
            "sources": sources,
            "elapsed": elapsed,
            "tokens": 0,
            "cost": 0.0,
            "details": {"mode": mode, "topic": topic},
        }
    }


