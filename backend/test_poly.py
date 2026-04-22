import requests
import time

def test_clob_api():
    # CLOB Host - often more stable than Gamma
    HOST = "https://clob.polymarket.com"
    
    try:
        # 1. First, we get the list of active markets
        print("📡 Fetching simplified markets from CLOB...")
        response = requests.get(f"{HOST}/markets", timeout=10)
        markets = response.json()
        
        # 2. Look for a Bitcoin or Trump market in the list
        relevant_markets = [m for m in markets if "Bitcoin" in m.get('question', '')]
        
        if relevant_markets:
            print(f"✅ Success! Found {len(relevant_markets)} Bitcoin markets.")
            m = relevant_markets[0]
            print(f"Market: {m['question']}")
            # CLOB markets provide token IDs which we use for live pricing
            print(f"Outcome Tokens: {m['outcomes']}")
        else:
            print("❓ Connected to CLOB, but no matching markets found in the first page.")
            
    except Exception as e:
        print(f"❌ CLOB API also unreachable: {e}")

test_clob_api()