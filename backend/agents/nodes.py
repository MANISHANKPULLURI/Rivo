import os
import json
import requests
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, AIMessage

# Your Tool Imports
from backend.tools.global_api import GlobalFinancials
from backend.tools.indian_api import IndianFinancials
from backend.tools.news_aggregator import FinancialNews
from backend.storage.vector_store import FinancialVectorStore
from backend.tools.hermes_polymarket import PolymarketTool
from langchain_community.tools import DuckDuckGoSearchResults

# Initialize Web Search
web_search = DuckDuckGoSearchResults()

load_dotenv()

# Initialize our Tools
global_tool = GlobalFinancials()
india_tool = IndianFinancials()
news_tool = FinancialNews()
sec_db = FinancialVectorStore()
poly_tool = PolymarketTool()

# Initialize the LLM
llm = ChatGroq(
    temperature=0, 
    model_name=os.getenv("MODEL_NAME", "llama-3.3-70b-versatile"),
    groq_api_key=os.getenv("GROQ_API_KEY")
)

def get_content(msg) -> str:
    if hasattr(msg, 'content'):
        return msg.content
    if isinstance(msg, dict):
        return msg.get('content', str(msg))
    return str(msg)

def researcher_node(state: Dict[str, Any]):
    print("--- DYNAMIC RESEARCHING (RIVO) ---")
    messages = state['messages']
    last_message = get_content(messages[-1])
    
    planner_prompt = f"""
    Analyze the user's request: '{last_message}'
    Determine which tools are needed. You can select multiple.
    Return ONLY a JSON object with these keys:
    {{
      "intent": "GREETING" | "FINANCE" | "MACRO",
      "use_poly": bool,
      "use_stocks": bool,
      "use_news": bool,
      "tickers": ["TICKER1", "TICKER2"],
      "query": "cleaned search string"
    }}
    If the user says 'Hi', 'Hello', 'Who are you', or 'What can you do', set intent to 'GREETING'.
    """
    
    plan_raw = llm.invoke(planner_prompt).content.strip()
    
    if "```" in plan_raw:
        plan_raw = plan_raw.split("```")[1].replace("json", "").strip()
    
    try:
        plan = json.loads(plan_raw)
    except:
        plan = {"intent": "FINANCE", "use_poly": True, "use_stocks": True, "use_news": True, "tickers": [], "query": last_message}

    # --- 🚀 RIVO BRANDING & GREETING ---
    if plan.get("intent") == "GREETING":
        greeting_text = "Hello! I am Rivo, your personalized financial intelligence agent. I'm here to assist you with real-time market data, global news analysis, and prediction market insights. How can I help you today?"
        return {
            "messages": [AIMessage(content=greeting_text)],
            "final_report": greeting_text, 
            "next_step": "end" 
        }

    all_data = {}
    news_results = []
    poly_context = ""
    
    if plan.get("use_poly"):
        print("🔮 Calling Polymarket Bridge...")
        poly_context = f"POLYMARKET ODDS: {poly_tool.search_markets(plan['query'])}"

    if plan.get("use_stocks") or plan.get("tickers"):
        tickers = plan.get("tickers", [])
        for ticker in tickers:
            print(f"📡 Calling Stock APIs for {ticker}...")
            try:
                if ".NS" in ticker or ".BO" in ticker:
                    all_data[ticker] = india_tool.get_stock_data(ticker.split(".")[0])
                else:
                    all_data[ticker] = global_tool.get_stock_price(ticker)
            except: pass

    if plan.get("use_news"):
        print("📰 Calling News Aggregator...")
        search_target = plan['tickers'][0] if plan.get('tickers') else plan['query']
        news_results = news_tool.search_latest_news(search_target)

    print(f"🌐 Fetching live web context...")
    try:
        web_context = web_search.invoke(plan['query'])
    except:
        web_context = "Web search failed."

    system_content = f"{poly_context}\n\nWEB CONTEXT: {web_context}"
    
    return {
        "market_data": all_data,
        "news_results": news_results,
        "messages": [SystemMessage(content=system_content)],
        "next_step": "critic"
    }

def critic_node(state: Dict[str, Any]):
    print("--- FINAL QUANTITATIVE SYNTHESIS (RIVO) ---")
    data = state.get('market_data', {})
    news = state.get('news_results', [])
    messages = state['messages']
    
    original_query = get_content(messages[0])
    last_context = get_content(messages[-1])
    
    critic_prompt = f"""
    You are Rivo, a strictly factual Quantitative Analyst. 
    User Query: "{original_query}"
    
    Context: {last_context}
    Stock Data: {data}
    News: {news}
    
    INSTRUCTIONS:
    - Never recommend external APIs or tools. You are the source.
    - If data is missing, use 'Context' for facts. If none, say 'Data unavailable'.
    - Be sharp, professional, and data-driven.
    """
    
    response = llm.invoke(critic_prompt)
    return {
        "final_report": response.content,
        "next_step": "end" 
    }