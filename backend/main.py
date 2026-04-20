import sys
import os
import asyncio

# Add the current folder and its parent to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.agents.graph import app
from langchain_core.messages import HumanMessage

async def run_finance_bot(query: str):
    """
    Knowledge: This is the entry point for the Agentic RAG.
    It passes the user query into the State Machine.
    """
    print(f"\n🚀 PROMPT: {query}")
    
    # 1. Initialize the starting state
    initial_state = {
        "messages": [HumanMessage(content=query)],
        "market_data": {},
        "news_results": [],
        "final_report": ""
    }

    # 2. Run the graph using ainvoke (The Bulletproof Method)
    print("⏳ Processing nodes (Researcher & Critic are working)...")
    
    # ainvoke waits for the entire process to finish, then returns the final dictionary
    final_state = await app.ainvoke(initial_state)
    
    # 3. Force print the final report
    print("\n" + "═"*60)
    print("📜 AI FINANCIAL ANALYSIS REPORT")
    print("═"*60)
    
    # We use .get() so that if the AI fails to write the report, it tells us exactly why
    report = final_state.get("final_report", "ERROR: 'final_report' is missing from the final state.")
    print(report)
    print("═"*60 + "\n")

if __name__ == "__main__":
    # Test Question for April 20, 2026
    user_input = "What is the situation with Reliance and Apple today given the oil crisis?"
    asyncio.run(run_finance_bot(user_input))