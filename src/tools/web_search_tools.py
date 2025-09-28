import os

from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchRun

# Attempt to import SearchAPIRun for SearchApi.io (SerpAPI alternative).
try:
    from langchain_community.tools.searchapi import SearchAPIRun
    SERPAPI_AVAILABLE = True
except ImportError:
    SERPAPI_AVAILABLE = False

# Attempt to import TavilySearchResults for Tavily web search.
try:
    from langchain_community.tools.tavily_search import TavilySearchResults
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

# duckduckgo_search: Performs a web search using DuckDuckGo (no API key required).
# Returns a list of web search result summaries or links.
duckduckgo_search = DuckDuckGoSearchRun(
    name="DuckDuckGoWebSearch",
    description="Performs a web search using DuckDuckGo."
)

# serpapi_search: Uses SearchApi.io (if available and API key is set) to perform a web search.
# Returns a list of web search result summaries or links.
searchapi_key = os.getenv("SEARCHAPI_API_KEY")
if SERPAPI_AVAILABLE and searchapi_key:
    try:
        serpapi_search = SearchAPIRun(api_wrapper_kwargs={"searchapi_api_key": searchapi_key})
    except Exception:
        serpapi_search = None
else:
    serpapi_search = None

# tavily_search: Uses Tavily (if available and API key is set) to perform a web search.
# Returns a list of web search result summaries or links.
tavily_key = os.getenv("TAVILY_API_KEY")
if TAVILY_AVAILABLE and tavily_key:
    try:
        tavily_search = TavilySearchResults(api_key=tavily_key)
    except Exception:
        tavily_search = None
else:
    tavily_search = None