"""Streamlit app orchestrating the multi-agent research workflow."""





from __future__ import annotations











import json





import time





from typing import Any, Dict, List











import os





import sys





from dotenv import load_dotenv





import streamlit as st











from src.agent.cleanup_agent import cleanup_archives





from src.agent.data_archiver import archive_state





from src.agent.orchestrator import create_research_plan





from src.agent.web_researcher import research_web





from src.agent.academic_researcher import research_academic_papers





from src.agent.news_analyzer import analyze_news





from src.agent.social_analyzer import analyze_social





from src.agent.financial_analyzer import analyze_financial





from src.agent.perplexity_researcher import research_perplexity





from src.agent.youtube_researcher import analyze_youtube





from src.agent.vector_pipeline import store_in_vector_db, retrieve_from_vector_db





from src.agent.synthesizer import generate_final_report





from src.graph.builder import build_graph





from src.utils.pdf_exporter import markdown_to_pdf_bytes

















PIPELINE = [





    ("orchestrator", "Planning orchestration", create_research_plan, "research_plan", True),





    ("web_researcher", "Performing web research", research_web, "web_results", True),





    ("academic_researcher", "Researching academic papers", research_academic_papers, "academic_results", True),





    ("news_analyzer", "Analyzing news", analyze_news, "news_results", True),





    ("social_analyzer", "Performing social media analysis", analyze_social, "social_sentiment", True),





    ("perplexity_researcher", "Researching using Perplexity", research_perplexity, "perplexity_results", True),





    ("youtube_researcher", "Analyzing YouTube videos", analyze_youtube, "youtube_results", True),





    ("financial_analyzer", "Performing financial analysis", analyze_financial, "financial_data", True),





    ("cleanup", "Cleaning up previous run", cleanup_archives, "cleanup_result", True),





    ("data_archiver", "Persisting results", archive_state, "archive_path", False),





    ("vector_store", "Indexing", store_in_vector_db, "vector_store_result", True),





    ("rag_retriever", "Semantic search", retrieve_from_vector_db, "rag_result", True),





    ("synthesizer", "Preparing final output", generate_final_report, "synthesizer_result", True),





]











SESSION_DEFAULTS = {





    "last_state": None,





    "last_totals": (0, 0.0, 0.0),





    "last_report": "",





    "last_pdf": None,





    "stored_progress": [],





}

















# --- Helper functions -----------------------------------------------------











def ensure_repo_path() -> None:





    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

















def show_agent_result(result: Any) -> str:





    if not result:





        return "No results."





    if isinstance(result, list):





        return "\n".join(str(item) for item in result)





    if isinstance(result, dict):





        lines: List[str] = []





        sources = result.get("sources", [])





        if sources:





            for source in sources:





                name = source.get("name", "source").replace("_", " ").title()





                lines.append(f"{name}:")





                items = source.get("items", [])





                if items:





                    for item in items:





                        lines.append(f"  - {item}")





                else:





                    lines.append("  (no data)")





                metadata = source.get("metadata", {})





                error = metadata.get("error")





                if error:





                    lines.append(f"  (error: {error})")





            details = result.get("details", {})





            detail_lines = [f"{k}: {v}" for k, v in details.items() if k != "topic"]





            if detail_lines:





                lines.append("Details: " + ", ".join(detail_lines))





        else:





            lines.append(json.dumps(result, ensure_ascii=False, indent=2))





        elapsed = result.get("elapsed")





        if elapsed is not None:





            lines.append(f"Time taken: {elapsed:.2f} seconds")





        tokens = result.get("tokens")





        if tokens is not None:





            lines.append(f"Tokens used: {tokens}")





        cost = result.get("cost")





        if cost is not None:





            lines.append(f"Cost: ${cost:.6f}")





        return "\n".join(lines)





    return str(result)

















def format_agent_metrics(result: Any) -> str:





    if isinstance(result, dict):





        parts: List[str] = []





        elapsed = result.get("elapsed")





        if isinstance(elapsed, (int, float)):





            parts.append(f"{elapsed:.2f}s")





        tokens = result.get("tokens")





        if isinstance(tokens, (int, float)) and tokens:





            parts.append(f"{tokens} tok")





        cost = result.get("cost")





        if isinstance(cost, (int, float)) and cost:





            parts.append(f"${cost:.6f}")





        return " | ".join(parts)





    return ""

















def aggregate_totals(state: Dict[str, Any]) -> tuple[int, float, float]:





    total_tokens = 0





    total_cost = 0.0





    total_time = 0.0





    for value in state.values():





        if isinstance(value, dict):





            total_tokens += int(value.get("tokens", 0) or 0)





            total_cost += float(value.get("cost", 0.0) or 0.0)





            total_time += float(value.get("elapsed", 0.0) or 0.0)





    return total_tokens, total_cost, total_time

















def render_progress(entries: List[Dict[str, Any]], container: Any) -> None:





    if not entries:





        container.info("Run a topic to see workflow progress.")





        return





    container.subheader("Workflow Progress")





    for entry in entries:





        label = entry.get("label", "Step")





        status = entry.get("status")





        if status == "success":





            block = container.success(f"[DONE] {label}")





            details = entry.get("details")





            if details:





                container.caption(details)





            note = entry.get("note")





            if note:





                container.caption(note)





            if entry.get("output"):





                with container.expander("Details", expanded=False):





                    st.text(entry["output"])





        elif status == "skip":





            reason = entry.get("reason", "Skipped")





            container.info(f"[SKIPPED] {label} - {reason}")





        elif status == "error":





            container.error(f"[ERROR] {label}")





            container.caption(entry.get("error", ""))

















# --- App setup ------------------------------------------------------------





ensure_repo_path()





dotenv_path = os.path.join(os.path.dirname(__file__), '.env')





load_dotenv(dotenv_path)











st.set_page_config(





    page_title="Agentic Deep Research",





    page_icon=":mag:",





    layout="wide",





)











for key, value in SESSION_DEFAULTS.items():





    if key not in st.session_state:





        st.session_state[key] = value











st.title("Agentic Deep Research Platform")











with st.sidebar:





    st.header("Configuration")





    mode = st.radio(





        "Research Mode",





        ["Simple", "Extended"],





        index=1,





        help="Simple: faster, fewer results. Extended: deeper dive.",





        key="mode_selector",





    )





    mode_key = "simple" if mode == "Simple" else "extended"





    st.divider()





    st.header("Run Statistics")





    tokens_placeholder = st.empty()





    cost_placeholder = st.empty()





    time_placeholder = st.empty()

















def update_run_statistics() -> None:





    total_tokens, total_cost, total_time = st.session_state["last_totals"]





    tokens_placeholder.metric("Total Tokens", f"{total_tokens:,}")





    cost_placeholder.metric("Total Cost", f"${total_cost:.6f}")





    time_placeholder.metric("Total Time", f"{total_time:.2f}s")

















update_run_statistics()











st.markdown("Enter a topic below and let the multi-agent system perform a deep dive.")











research_graph = build_graph()











controls_col, results_col = st.columns([2, 3], gap='large')

with controls_col:
    topic = st.text_input("Enter the research topic:", "", placeholder="e.g., 'The future of AI in healthcare'", key="topic_input")
    start_clicked = st.button("Start Research", type="primary")
    progress_container = st.container()

with results_col:
    results_container = st.container()











if start_clicked:





    if not topic.strip():





        st.error("Please enter a topic to research.")





    else:





        st.session_state.update({





            "last_state": None,





            "last_report": "",





            "last_pdf": None,





            "stored_progress": [],





            "last_totals": (0, 0.0, 0.0),





        })





        update_run_statistics()











        progress_container.empty()





        status_container = progress_container





        status_container.subheader("Workflow Progress")





        placeholders = {step_id: status_container.empty() for step_id, _, _, _, _ in PIPELINE}











        state: Dict[str, Any] = {"topic": topic, "mode": mode_key}





        progress_log: List[Dict[str, Any]] = []





        try:





            for step_id, label, func, result_key, show_output in PIPELINE:





                if step_id == "financial_analyzer" and mode_key == "simple":





                    placeholders[step_id].info(f"[SKIPPED] {label} (simple mode)")





                    progress_log.append({





                        "label": label,





                        "status": "skip",





                        "reason": "Skipped in simple mode",





                    })





                    st.session_state["stored_progress"] = progress_log.copy()





                    continue











                placeholders[step_id].info(f"[RUNNING] {label}")





                start_time = time.time()





                result = func(state)





                if result:





                    state.update(result)





                elapsed = time.time() - start_time











                value = state.get(result_key)





                output_text = show_agent_result(value) if show_output else ""





                metrics = format_agent_metrics(value)





                details = " | ".join(filter(None, [metrics, f"Step time: {elapsed:.2f}s"]))





                note = None





                if step_id == "data_archiver" and isinstance(state.get("archive_path"), str):





                    note = f"Results archived at: {state['archive_path']}"











                container = placeholders[step_id].container()





                container.success(f"[DONE] {label}")





                if details:





                    container.caption(details)





                if note:





                    container.caption(note)





                if output_text:





                    with container.expander("Details", expanded=False):





                        st.text(output_text)





                progress_log.append({





                    "label": label,





                    "status": "success",





                    "details": details,





                    "note": note,





                    "output": output_text or "",





                    "elapsed": elapsed,





                })





                st.session_state["stored_progress"] = progress_log.copy()





        except Exception as exc:





            progress_log.append({"label": label, "status": "error", "error": str(exc)})





            st.session_state["stored_progress"] = progress_log





            err_placeholder = placeholders.get(step_id)





            if err_placeholder is not None:





                with err_placeholder.container():





                    st.error(f"[ERROR] {label}")





                    st.caption(str(exc))





            st.error(f"An error occurred: {exc}")





        else:





            st.session_state["stored_progress"] = progress_log





            st.session_state["last_state"] = state





            totals = aggregate_totals(state)





            st.session_state["last_totals"] = totals





            update_run_statistics()











            report = state.get("final_report", "")





            if report:





                st.session_state["last_report"] = report





                st.session_state["last_pdf"] = markdown_to_pdf_bytes(report, title=f"Research Report: {topic}")





            else:





                st.session_state["last_report"] = ""





                st.session_state["last_pdf"] = None











            st.success("Workflow completed successfully.")





else:





    progress_container.empty()











render_progress(st.session_state.get("stored_progress", []), progress_container)











with results_container:
    st.subheader("Results")
    
    
    
    
    
    final_state = st.session_state.get("last_state")
    
    
    
    
    
    if final_state:
    
    
    
    
    
        report = st.session_state.get("last_report", "")
    
    
    
    
    
        pdf_bytes = st.session_state.get("last_pdf")
    
    
    
    
    
        with st.expander("Final Output", expanded=False):
    
    
    
    
    
            if report:
    
    
    
    
    
                st.markdown(report)
    
    
    
    
    
            else:
    
    
    
    
    
                st.info("No report generated yet.")
    
    
    
    
    
        if pdf_bytes and report:
    
    
    
    
    
            st.download_button(
    
    
    
    
    
                label="Download PDF",
    
    
    
    
    
                data=pdf_bytes,
    
    
    
    
    
                file_name="research_report.pdf",
    
    
    
    
    
                mime="application/pdf",
    
    
    
    
    
                key="download_pdf",
    
    
    
    
    
            )
    
    
    
    
    
        totals = st.session_state.get("last_totals", (0, 0.0, 0.0))
    
    
    
    
    
        st.caption(
    
    
    
    
    
            f"Session totals -- Tokens: {totals[0]:,} | Cost: ${totals[1]:.6f} | Time: {totals[2]:.2f}s"
    
    
    
    
    
        )
    
    
    
    
    
    else:
    
    
    
    
    
        st.info("Run a topic to see results and download the final report.")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
