# This module exports academic research tools for use by research agents.
__all__ = ["arxiv_tool", "scholar_search", "fetch_arxiv_structured"]
# src/tools/academic_tools.py
from typing import Any, Dict, List, Tuple

from langchain_community.tools import ArxivQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities.arxiv import ArxivAPIWrapper
from src.utils.structured_data import build_structured_record

# arxiv_tool: Provides an interface to search and retrieve academic papers from arXiv.org.
# Returns a list of relevant paper summaries or metadata for a given query.
arxiv_tool = ArxivQueryRun(load_all_available_meta=True, doc_content_chars_max=None)

# scholar_search: Uses DuckDuckGo to search Google Scholar for academic papers related to a query.
# Returns a list of search result summaries or links for academic content.
scholar_search = DuckDuckGoSearchRun(
    name="GoogleScholarSearch",
    description="Searches Google Scholar for academic papers.",
)


def fetch_arxiv_structured(query: str, max_results: int) -> Tuple[List[Dict[str, Any]], str | None]:
    """Return structured arXiv results including metadata and optional full text."""
    wrapper = ArxivAPIWrapper(
        top_k_results=max_results,
        load_all_available_meta=True,
        continue_on_failure=True,
        doc_content_chars_max=None,
    )
    try:
        search_results = list(wrapper._fetch_results(query))  # type: ignore[attr-defined]
    except Exception as exc:  # pragma: no cover - third-party failure
        return [], str(exc)

    content_map: Dict[str, str] = {}
    if search_results:
        try:
            fulltext_wrapper = ArxivAPIWrapper(
                top_k_results=max_results,
                load_all_available_meta=True,
                continue_on_failure=True,
                doc_content_chars_max=None,
            )
            for doc in fulltext_wrapper.load(query):
                title = doc.metadata.get("Title")
                if title and doc.page_content:
                    content_map.setdefault(title, doc.page_content)
        except Exception:  # pragma: no cover - optional dependency (PyMuPDF)
            pass

    structured_results: List[Dict[str, Any]] = []
    for result in search_results:
        published = getattr(result, "published", None)
        if published is not None and hasattr(published, "date"):
            published_str = published.date().isoformat()
        elif published is not None:
            published_str = str(published)
        else:
            published_str = None

        authors = [
            getattr(author, "name", str(author))
            for author in getattr(result, "authors", [])
            if getattr(author, "name", str(author))
        ]
        title = getattr(result, "title", "")
        summary = getattr(result, "summary", "")
        content = content_map.get(title) or summary
        structured_results.append(
            build_structured_record(
                title=title,
                summary=summary,
                content=content,
                source=getattr(result, "entry_id", ""),
                published_date=published_str,
                authors=authors,
                pdf_url=getattr(result, "pdf_url", None),
            )
        )

    return structured_results, None

# Additional academic tools can be added below as needed for other sources or APIs.
