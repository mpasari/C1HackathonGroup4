# This module provides tools for retrieving news articles from APIs and web search.
from langchain_community.tools import DuckDuckGoSearchRun
import os

# Attempt to import NewsAPIWrapper for direct news API access.
try:
    from langchain_community.tools.news_api import NewsAPIWrapper
    NEWS_API_AVAILABLE = True
except ImportError:
    NEWS_API_AVAILABLE = False

# news_api_tool: Uses NewsAPI (if available and API key is set) to fetch recent news articles for a query.
# Returns a list of news article summaries or links.
news_api_key = os.getenv("NEWS_API_KEY")
if NEWS_API_AVAILABLE and news_api_key:
    news_api_tool = NewsAPIWrapper(api_key=news_api_key)
else:
    news_api_tool = None

# news_search: Uses DuckDuckGo to search for recent news articles as a fallback if NewsAPI is not available.
# Returns a list of news article summaries or links.
news_search = DuckDuckGoSearchRun(
    name="NewsSearch",
    description="Searches the web for recent news articles.",
)

# Example usage:
#   news_api_tool.run(query) or news_search.run(query)
