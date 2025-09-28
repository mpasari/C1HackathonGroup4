import time
from typing import Any, Dict, List

# This module defines the financial analyzer agent, which retrieves financial news if the topic is finance-related.
from src.graph.state import ResearchState
from src.tools.financial_tools import is_financial_intent, get_financial_news


def _normalize_results(results: Any, limit: int) -> List[Any]:
    if isinstance(results, list):
        return results[:limit]
    if isinstance(results, str):
        return [results][:limit]
    return []


def analyze_financial(state: ResearchState) -> dict:
    """
    The financial analyzer agent retrieves financial news for the given topic if financial intent is detected.
    Returns a dictionary with raw financial news items and metadata.
    """
    start = time.time()
    topic = state.get("topic", "")
    mode = state.get('mode', 'extended')
    num_items = 2 if mode == 'simple' else 10

    intent_detected, intent_metrics = is_financial_intent(topic)
    items: List[Any] = []
    metadata: Dict[str, Any] = {
        "limit": num_items,
        "topic": topic,
        "intent_detected": intent_detected,
        "intent_prompt_tokens": intent_metrics.prompt_tokens,
        "intent_completion_tokens": intent_metrics.completion_tokens,
        "intent_total_tokens": intent_metrics.total_tokens,
        "intent_cost": intent_metrics.cost,
        "intent_duration": intent_metrics.duration,
    }

    if intent_detected:
        raw_news = get_financial_news(topic)
        items = _normalize_results(raw_news, num_items)
        metadata["item_count"] = len(items)
    else:
        metadata["item_count"] = 0
        metadata["note"] = "no_financial_intent_detected"

    elapsed = time.time() - start
    return {
        "financial_data": {
            "sources": [
                {
                    "name": "financial_news",
                    "items": items,
                    "metadata": metadata,
                }
            ],
            "elapsed": elapsed,
            "tokens": intent_metrics.total_tokens,
            "cost": intent_metrics.cost,
            "details": {
                "mode": mode,
                "topic": topic,
                "intent_detected": intent_detected,
            },
        }
    }

