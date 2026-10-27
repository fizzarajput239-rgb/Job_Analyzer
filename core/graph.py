"""LangGraph workflow: START -> extract -> classify -> skills -> report -> END."""
from langgraph.graph import StateGraph, START, END

from core.nodes import (
    extract_info_node, classify_job_node, analyze_skills_node, generate_report_node,
)
from core.state import GraphState
from core.validation import validate_job_description
from core.models import HiringReport


def build_graph():
    g = StateGraph(GraphState)
    g.add_node("extract_info", extract_info_node)
    g.add_node("classify_job", classify_job_node)
    g.add_node("analyze_skills", analyze_skills_node)
    g.add_node("generate_report", generate_report_node)

    g.add_edge(START, "extract_info")
    g.add_edge("extract_info", "classify_job")
    g.add_edge("classify_job", "analyze_skills")
    g.add_edge("analyze_skills", "generate_report")
    g.add_edge("generate_report", END)
    return g.compile()


def analyze_job_description(text) -> HiringReport:
    """Validate -> graph run -> HiringReport. Error par ValueError/RuntimeError raise karta hai."""
    clean = validate_job_description(text)
    final_state = build_graph().invoke({"job_description": clean})
    if final_state.get("error"):
        raise RuntimeError(final_state["error"])
    return final_state["report"]
