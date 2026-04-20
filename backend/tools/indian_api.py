import yfinance as yf
from dotenv import load_dotenv

load_dotenv()

class IndianFinancials:
    """
    Knowledge: This class abstracts the complexity of the Indian Stock Market.
    It handles ticker formatting and data normalization.
    """
    def __init__(self):
        # We don't need an API key for yfinance, but we keep the structure 
        # consistent with GlobalFinancials for 'Polymorphism' (OOP concept).
        pass

    def get_stock_data(self, ticker: str):
        """
        Encapsulation: This method handles the logic of NSE vs BSE.
        """
        # Logic: If no exchange is specified, default to NSE (.NS)
        if not (ticker.endswith(".NS") or ticker.endswith(".BO")):
            formatted_ticker = f"{ticker.upper()}.NS"
        else:
            formatted_ticker = ticker.upper()

        try:
            stock = yf.Ticker(formatted_ticker)
            info = stock.info
            
            # Normalization: We map messy yfinance keys to clean, standard names.
            # This ensures the AI sees the same 'shape' of data for India and the US.
            return {
                "symbol": info.get("symbol"),
                "current_price": info.get("currentPrice"),
                "currency": info.get("currency"), # Usually 'INR'
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "day_high": info.get("dayHigh"),
                "day_low": info.get("dayLow"),
                "exchange": "NSE" if ".NS" in formatted_ticker else "BSE"
            }
        except Exception as e:
            return {"error": f"Indian Market Fetch Failed: {str(e)}"}

# Example: 
# tool = IndianFinancials()
# print(tool.get_stock_data("RELIANCE"))