import os
from langgraph.graph import StateGraph, END

# ==========================================
# Enable LangSmith Tracing Dynamically
# ==========================================
# يفحص os.environ مباشرة بصرف النظر عن مصدر التعيين
api_key = os.environ.get("LANGCHAIN_API_KEY")
if api_key:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = os.environ.get("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    os.environ["LANGCHAIN_PROJECT"] = os.environ.get("LANGCHAIN_PROJECT", "counseling-institute-assistant")


# 1. Import state and agents AFTER setting env variables
from models import state
from agents import rewriter_agent, response_agent


# ==========================================
# Build the LangGraph Workflow
# ==========================================

workflow = StateGraph(state)

# Add Nodes
workflow.add_node("rewrite_query", rewriter_agent)
workflow.add_node("generate_response", response_agent)

# Define Edges
workflow.set_entry_point("rewrite_query")
workflow.add_edge("rewrite_query", "generate_response")
workflow.add_edge("generate_response", END)

# Compile Graph
app = workflow.compile()