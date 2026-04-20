import os
import requests

class GlobalFinancials:
    def __init__(self):
        self.api_key = os.getenv("ALPHA_VANTAGE_KEY")
        self.base_url = "https://www.alphavantage.co/query"

    def get_stock_price(self, ticker):
        print(f"📡 Fetching Global Data for {ticker} via Alpha Vantage...")
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params).json()
            return response.get("Global Quote", {"Error": "No data found for ticker"})
        except Exception as e:
            return {"Error": f"API Request failed: {str(e)}"}