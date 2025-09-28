# This module provides tools for retrieving social sentiment and tweets using the Twitter API.
import os
import requests

from src.utils.structured_data import build_structured_record

# Twitter API bearer token is loaded from environment variables.
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")


def twitter_search(query, max_results=10):
    """
    Searches recent tweets using Twitter API v2 for a given query string.
    Returns a list of structured tweet records (up to max_results).
    """
    if not TWITTER_BEARER_TOKEN:
        return []
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    params = {
        "query": query,
        "max_results": max_results,
        "tweet.fields": "created_at,author_id,text",
        "expansions": "author_id",
        "user.fields": "name,username",
    }
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        return []

    data = resp.json()
    tweets = data.get("data", [])
    users = {user["id"]: user for user in data.get("includes", {}).get("users", [])}

    structured = []
    for tweet in tweets:
        author_id = tweet.get("author_id")
        user = users.get(author_id)
        if user:
            authors = [user.get("name") or user.get("username") or author_id]
            username = user.get("username")
        else:
            authors = [author_id] if author_id else []
            username = None
        tweet_url = (
            f"https://twitter.com/{username}/status/{tweet['id']}"
            if username
            else f"https://twitter.com/i/web/status/{tweet['id']}"
        )
        text = tweet.get("text", "")
        structured.append(
            build_structured_record(
                title=text[:120] if text else None,
                summary=text,
                content=text,
                source=tweet_url,
                published_date=tweet.get("created_at"),
                authors=authors,
            )
        )
    return structured
