# workflow.py

from langgraph.graph import StateGraph, END

# 1. Import state definition from your prompt file
from models import state

# 2. Import agents from agents file
from agents import rewriter_agent, response_agent


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


# ==========================================
# Execution Example
# ==========================================

initial_input = {
    "user_query": "ايه هي المحاور الرئيسية لكورس المراهقين؟",
    "chat_history": []
}

# Run graph execution
result = app.invoke(initial_input)

print("\n--- Final Assistant Response ---")
print(result.get("response"))