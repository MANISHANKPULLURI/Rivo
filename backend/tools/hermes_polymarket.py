import requests
import json

class PolymarketTool:
    def __init__(self):
        self.gamma_url = "https://gamma-api.polymarket.com"
        self.clob_url = "https://clob.polymarket.com"

    def search_markets(self, query: str):
        """Finds events/markets based on a user's question."""
        endpoint = f"{self.gamma_url}/public-search"
        params = {"q": query}
        
        try:
            response = requests.get(endpoint, params=params)
            data = response.json()
            
            refined_results = []
            for item in data:
                # Polymarket often returns 'events' which contain 'markets'
                if 'markets' in item:
                    for market in item['markets']:
                        # FIX: Double-encoded field parsing
                        prices = json.loads(market.get('outcomePrices', '["0", "0"]'))
                        
                        refined_results.append({
                            "question": market.get('question'),
                            "yes_prob": f"{float(prices[0]) * 100:.1f}%",
                            "no_prob": f"{float(prices[1]) * 100:.1f}%",
                            "volume": f"${float(market.get('volume', 0)):,.0f}",
                            "status": "Active" if not market.get('closed') else "Closed"
                        })
            return refined_results[:5] # Top 5 relevant markets
        except Exception as e:
            return f"Polymarket Search Error: {e}"