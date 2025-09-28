
# This module defines the orchestrator agent, which creates a research plan for the given topic.
from src.graph.state import ResearchState

def create_research_plan(state: ResearchState) -> dict:
	"""
	The orchestrator agent creates a research plan for the given topic, outlining which agents will be used.
	Returns a dictionary with the research plan as a string.
	"""
	topic = state.get("topic", "")
	plan = f"Research plan for topic: {topic}\n- Web research\n- Academic papers\n- News\n- Social sentiment\n- Financial data (if relevant)"
	return {"research_plan": plan}
