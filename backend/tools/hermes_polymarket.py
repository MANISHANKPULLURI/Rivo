import requests
import json

class PolymarketTool:
    def __init__(self):
        # 🟢 YOUR BRIDGE: Bypasses regional blocks for all Polymarket domains
        self.bridge_url = "https://rivo.manishankmani.workers.dev"

    def search_markets(self, query: str):
        """
        Comprehensive search using the /events endpoint. 
        This groups all outcomes for a question together for a complete view.
        """
        # Calling the /events endpoint via your bridge
        endpoint = f"{self.bridge_url}/events"
        params = {
            "q": query,
            "closed": "false",  # Only active markets
            "limit": 5          # Top 5 most relevant event groups
        }
        
        try:
            print(f"📡 Researching ALL Polymarket events for: {query}")
            response = requests.get(endpoint, params=params, timeout=12)
            
            if response.status_code != 200:
                return f"Bridge Connection Error (Status {response.status_code})"
            
                
            events = response.json()

            if not events or len(events) == 0:
                return "The market is currently undergoing a technical migration to pUSD. No live odds available for this specific query right now."
            full_analysis = []

            for event in events:
                event_title = event.get('title', 'Unknown Event')
                markets = event.get('markets', [])
                
                # We collect all outcomes within this event
                outcomes_summary = []
                for m in markets:
                    # Parse outcome labels and their current prices
                    labels = json.loads(m.get('outcomes', '[]'))
                    prices = json.loads(m.get('outcomePrices', '[]'))
                    
                    # Match labels to prices (e.g., "Trump: 52%")
                    for i, price in enumerate(prices):
                        name = labels[i] if i < len(labels) else f"Option {i}"
                        prob = f"{float(price) * 100:.1f}%"
                        outcomes_summary.append(f"{name}: {prob}")

                full_analysis.append({
                    "question": event_title,
                    "probabilities": " | ".join(outcomes_summary),
                    "total_volume": f"${float(event.get('volume', 0)):,.0f}",
                    "description": event.get('description', '')[:200] + "..."
                })

            return full_analysis if full_analysis else "No matching prediction markets found."

        except Exception as e:
            print(f"❌ Polymarket Global Tool Error: {e}")
            return f"Error: {str(e)}"

# --- Quick Test ---
if __name__ == "__main__":
    tool = PolymarketTool()
    # Test with a non-crypto query to verify multi-outcome handling
    print(json.dumps(tool.search_markets("Election"), indent=2))