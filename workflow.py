import os
from langgraph.graph import StateGraph, END
from langsmith import traceable
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
class workflow:
    def __init__(self):
        self.rewriter_agent = rewriter_agent
        self.response_agent = response_agent

    @property
    @traceable
    def compile(self):
        graph = StateGraph(state)

        # Add Nodes
        graph.add_node("rewrite_query", self.rewriter_agent)
        graph.add_node("generate_response", self.response_agent)

        # Define Edges
        graph.set_entry_point("rewrite_query")
        graph.add_edge("rewrite_query", "generate_response")
        graph.add_edge("generate_response", END)
        return graph.compile()
    
# Compile Graph
app = workflow().compile