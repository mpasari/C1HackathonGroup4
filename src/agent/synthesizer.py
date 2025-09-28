"""LLM-backed synthesizer agent that composes the final report."""
from __future__ import annotations

import json
import os

from src.graph.state import ResearchState
from src.utils.llm_registry import invoke_llm


def load_synthesizer_prompt(mode: str = "extended") -> str:
    """Return the report-writing prompt tailored to *mode*."""
    if mode == "simple":
        prompt_file = "../prompts/synthesizer_prompt_simple.txt"
    else:
        prompt_file = "../prompts/synthesizer_prompt.txt"
    prompt_path = os.path.join(os.path.dirname(__file__), prompt_file)
    with open(os.path.abspath(prompt_path), "r", encoding="utf-8") as handle:
        return handle.read()


def _serialize_for_prompt(value: object) -> str:
    """Convert nested agent output into a JSON string suitable for prompting."""
    try:
        return json.dumps(value, ensure_ascii=False, indent=2)
    except TypeError:
        return str(value)


def gather_agent_outputs(state: ResearchState) -> str:
    """Collect agent outputs from *state* in a markdown-friendly format."""
    sections = []
    for key, label in [
        ("research_plan", "Research Plan"),
        ("web_results", "Web Results"),
        ("academic_results", "Academic Results"),
        ("news_results", "News Results"),
        ("social_sentiment", "Social Sentiment"),
        ("financial_data", "Financial Data"),
        ("vector_store_result", "Vector Store"),
        ("rag_result", "RAG Context"),
    ]:
        value = state.get(key)
        if value:
            text = _serialize_for_prompt(value)
            sections.append(f"## {label}\n{text}")
    return "\n\n".join(sections)


def generate_final_report(state: ResearchState, mode: str = "extended") -> dict:
    """Call the synthesiser LLM to produce the final report for *state*."""
    prompt_template = load_synthesizer_prompt(mode)
    topic = state.get("topic", "")
    agent_outputs = gather_agent_outputs(state)
    prompt = prompt_template.format(topic=topic, agent_outputs=agent_outputs)

    temperature = 0.0 if mode == "simple" else 0.2
    response, metrics = invoke_llm("synthesiser", prompt, temperature=temperature)
    report = response.content.strip()

    result_payload = {
        "sources": [
            {
                "name": "synthesizer",
                "items": [],
                "metadata": {"note": "See final report text"},
            }
        ],
        "elapsed": metrics.duration,
        "tokens": metrics.total_tokens,
        "cost": metrics.cost,
        "details": {
            "model": metrics.model,
            "prompt_tokens": metrics.prompt_tokens,
            "completion_tokens": metrics.completion_tokens,
            "truncated": metrics.truncated,
        },
    }

    return {"final_report": report, "synthesizer_result": result_payload}
