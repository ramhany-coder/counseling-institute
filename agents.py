# agents.py
from config import settings
from langchain_groq import ChatGroq
# 1. Import necessary components from your prompt/state module
from prompt import (
    REWRITE_PROMPT,
    SYSTEM_RESPOND_PROMPT,
    query_rewrite_extend,
    system_prompt_extend
)
from models import state
# 2. Import your LLM model from your models module
llm_response = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=settings.llm_api,
        )
llm_rewrite =  ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=settings.llm_api,
        )

from langchain_core.messages import SystemMessage, HumanMessage


# ==========================================
# Agent 1: Query Rewriter Agent
# ==========================================
def rewriter_agent(state_data: state) -> dict:
    """
    Extracts user_query and chat_history from State, builds the prompt 
    using query_rewrite_extend, and invokes the LLM to return a search query.
    """
    user_input = state_data.get("user_query", "")
    chat_history = state_data.get("chat_history", [])

    # Format the prompt using the helper from prompt_file
    formatted_user_prompt = query_rewrite_extend(
        user_input=user_input, 
        chat_history=chat_history
    )

    messages = [
        SystemMessage(content=REWRITE_PROMPT),
        HumanMessage(content=formatted_user_prompt)
    ]

    # Invoke LLM
    response = llm_rewrite.invoke(messages)
    
    # Store rewritten query (or pass it downstream)
    rewritten_query = response.content.strip()

    return {
        "rewritten_query": rewritten_query
    }


# ==========================================
# Agent 2: Responding Agent (Secretary)
# ==========================================
def response_agent(state_data: state) -> dict:
    """
    Extracts user_query, chat_history, and context/retrieved content from State,
    builds the secretary prompt via system_prompt_extend, and gets the final response.
    """
    user_input = state_data.get("rewritten_query", "")
    chat_history = state_data.get("chat_history", "")
    content = state_data.get("content", "")  # Retained context if passed via state

    # Format the prompt using the helper from prompt_file
    formatted_user_prompt = system_prompt_extend(
        user_input=user_input,
        chat_history=str(chat_history),
        content=content
    )

    messages = [
        SystemMessage(content=SYSTEM_RESPOND_PROMPT),
        HumanMessage(content=formatted_user_prompt)
    ]

    # Invoke LLM
    response = llm_response.invoke(messages)

    return {
        "response": response.content,
        "chat_history": [HumanMessage(content=user_input), response]
    }