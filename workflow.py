import os
from langgraph.graph import StateGraph, END

# 1. Import configurations & state definition
from config import settings
from models import state

# 2. Import agents from agents file
from agents import rewriter_agent, response_agent


# ==========================================
# Enable LangSmith Tracing
# ==========================================
if getattr(settings, "langchain_api_key", None):
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
    os.environ["LANGCHAIN_PROJECT"] = getattr(settings, "langchain_project", "counseling-institute-assistant")


# ==========================================
# Build the LangGraph Workflow
# ==========================================

# Initialize graph with the State schema
workflow = StateGraph(state)

# Add Nodes (Only Rewriter & Responder)
workflow.add_node("rewrite_query", rewriter_agent)
workflow.add_node("generate_response", response_agent)

# Define Graph Edges (Direct Pipeline)
workflow.set_entry_point("rewrite_query")
workflow.add_edge("rewrite_query", "generate_response")
workflow.add_edge("generate_response", END)

# Compile Graph
app = workflow.compile()