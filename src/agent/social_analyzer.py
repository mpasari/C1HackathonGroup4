import time
from typing import Any, Dict, List

# This module defines the social analyzer agent, which analyzes social sentiment using Twitter data.
from src.graph.state import ResearchState
from src.tools.social_tools import twitter_search


def analyze_social(state: ResearchState) -> dict:
    """
    The social analyzer agent analyzes social sentiment for the given topic using the Twitter API.
    Returns a dictionary with raw tweet data and metadata.
    """
    start = time.time()
    topic = state.get("topic", "")
    mode = state.get('mode', 'extended')
    num_items = 2 if mode == 'simple' else 10
    tweets = twitter_search(topic, max_results=num_items)

    elapsed = time.time() - start
    return {
        "social_sentiment": {
            "sources": [
                {
                    "name": "twitter",
                    "items": tweets,
                    "metadata": {
                        "limit": num_items,
                        "item_count": len(tweets),
                        "query": topic,
                    },
                }
            ],
            "elapsed": elapsed,
            "tokens": 0,
            "cost": 0.0,
            "details": {"mode": mode, "topic": topic},
        }
    }

