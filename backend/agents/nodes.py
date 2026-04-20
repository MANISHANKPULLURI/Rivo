import os
import json
import requests
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage

# Your Tool Imports
from backend.tools.global_api import GlobalFinancials
from backend.tools.indian_api import IndianFinancials
from backend.tools.news_aggregator import FinancialNews
from backend.storage.vector_store import FinancialVectorStore
from backend.tools.hermes_polymarket import PolymarketTool # Ensure this file exists
from langchain_community.tools import DuckDuckGoSearchResults

# Initialize Web Search
web_search = DuckDuckGoSearchResults()

load_dotenv()

# Initialize our Tools
global_tool = GlobalFinancials()
india_tool = IndianFinancials()
news_tool = FinancialNews()
sec_db = FinancialVectorStore()
poly_tool = PolymarketTool() # NEW: Initialize Polymarket

# Initialize the LLM
llm = ChatGroq(
    temperature=0, 
    model_name=os.getenv("MODEL_NAME", "llama-3.3-70b-versatile"),
    groq_api_key=os.getenv("GROQ_API_KEY")
)

def researcher_node(state):
    print("--- RESEARCHING DATA ---")
    messages = state['messages']
    
    # 🚨 THE FIX: Bulletproof way to read message content (Handles Objects & Dicts)
    last_message = messages[-1].content if hasattr(messages[-1], 'content') else messages[-1].get("content", "")
    
    # 1. SMART EXTRACTION: Tickers vs. Polymarket vs. Macro
    extraction_prompt = f"""
    Analyze the user's request: '{last_message}'
    - If they ask about odds, chances, probabilities, or 'will X happen', return 'POLYMARKET'.
    - If they ask for 'today's news' or 'market update', return 'MACRO'.
    - If they mention specific companies, return the tickers (append .NS for Indian stocks).
    - Otherwise, return 'NONE'.
    Return ONLY the category or comma-separated tickers.
    """
    intent = llm.invoke(extraction_prompt).content.strip().upper()

    all_data = {}
    news = []
    prediction_context = ""
    web_query = last_message

    # 2. POLYMARKET LOGIC
    if "POLYMARKET" in intent:
        print("🔮 Searching Polymarket for odds...")
        poly_data = poly_tool.search_markets(last_message)
        prediction_context = f"POLYMARKET ODDS: {poly_data}"
        web_query = last_message

    # 3. TICKER API LOGIC
    elif "MACRO" not in intent and "NONE" not in intent:
        tickers = [t.strip() for t in intent.split(",") if t.strip()]
        for ticker in tickers:
            print(f"📡 Fetching data for {ticker}...")
            try:
                if ".NS" in ticker or ".BO" in ticker or "NSE" in last_message.upper():
                    clean_ticker = ticker.replace(".NS", "").replace(".BO", "")
                    all_data[ticker] = india_tool.get_stock_data(clean_ticker)
                else:
                    all_data[ticker] = global_tool.get_stock_price(ticker)
            except: pass
        try:
            news = news_tool.search_latest_news(tickers[0])
        except: pass

    # 4. PROMPT-BASED WEB FETCHING
    print(f"🌐 Fetching live web context for: '{web_query}'")
    try:
        web_context = web_search.invoke(web_query) 
    except:
        web_context = "Web search failed."

    # 5. Get Deep Fundamental Memory (SEC)
    try:
        raw_results = sec_db.query_knowledge(last_message)
        fundamental_context = " | ".join(raw_results['documents'][0]) if raw_results and 'documents' in raw_results else "No SEC Data."
    except:
        fundamental_context = "SEC Database offline."
    
    # Combined intelligence for the Critic
    system_content = f"{prediction_context}\n\nSEC DATA: {fundamental_context}\n\nOPEN WEB CONTEXT: {web_context}"
    
    return {
        "market_data": all_data,
        "news_results": news,
        "messages": [SystemMessage(content=system_content)],
        "next_step": "critic"
    }

def critic_node(state):
    print("--- CRITIQUING DATA ---")
    data = state.get('market_data', {})
    news = state.get('news_results', [])
    messages = state['messages']
    
    # Bulletproof reading for Critic
    original_query = messages[0].content if hasattr(messages[0], 'content') else messages[0].get("content", "")
    last_msg_content = messages[-1].content if hasattr(messages[-1], 'content') else messages[-1].get("content", "")
    
    critic_prompt = f"""
    You are a strictly factual Quantitative Analyst. 
    User Query: "{original_query}"
    
    Gathered Data: {data}
    Short-term News: {news}
    Web/SEC/Polymarket Context: {last_msg_content}
    
    INSTRUCTIONS:
    1. If Polymarket data is present, emphasize the "Probability of Event" as the Wisdom of the Crowd.
    2. Synthesize hard numbers with prediction odds.
    3. MATH CHECK: Flag any impossible 52-week high/low data.
    
    ### 🔌 DATA SOURCES & APIs USED:
    * Prediction Markets: Polymarket Gamma API
    * Global Market Data: Alpha Vantage API
    * Indian Market Data: IndianFinancials Tool (NSE)
    * Fundamental Memory: Vector Store (SEC Filings)
    * Analysis Engine: Groq API (Llama-3.3-70b-versatile)
    """
    
    response = llm.invoke(critic_prompt)
    
    return {
        "final_report": response.content,
        "next_step": "end" 
    }