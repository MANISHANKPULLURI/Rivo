from typing import TypedDict, Annotated, List
import operator
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    # This is the 'Filing Cabinet'
    messages: Annotated[List[BaseMessage], operator.add]
    market_data: dict
    news_results: list
    
    # THE MISSING KEY: This tells LangGraph "Do not throw the report away!"
    final_report: str 
    next_step: str