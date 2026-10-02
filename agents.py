# agents.py
from config import settings
from langchain_openai import ChatOpenAI
# 1. Import necessary components from your prompt/state module
from prompt import (
    SYSTEM_RESPOND_PROMPT,
    system_prompt_extend
)
from models import state
# 2. Import your LLM model from your models module
# glm-5.x always thinks before answering; low effort keeps replies fast.
llm_response = ChatOpenAI(
        model=settings.zai_model,
        api_key=settings.zai_api_key,
        base_url=settings.zai_base_url,
        temperature= 0.2,
        reasoning_effort="low"
        )

from langchain_core.messages import SystemMessage, HumanMessage


# ==========================================
# Responding Agent (Secretary)
# ==========================================
def response_agent(state_data: state) -> dict:
    """
    Extracts user_query, chat_history, and context/retrieved content from State,
    builds the secretary prompt via system_prompt_extend, and gets the final response.
    """
    user_input = state_data.get("user_query", "")
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