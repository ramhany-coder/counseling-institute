
from typing import Optional , Annotated
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

class state (TypedDict):
    user_query : Optional[str]
    chat_history : Annotated[str,add_messages]
    response : Optional[str]
    

