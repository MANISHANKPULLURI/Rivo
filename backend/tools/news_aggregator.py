import os
import finnhub
from datetime import datetime, timedelta

class FinancialNews:
    def __init__(self):
        self.api_key = os.getenv("FINNHUB_API_KEY")
        self.client = finnhub.Client(api_key=self.api_key)

    def search_latest_news(self, ticker):
        print(f"📰 Fetching Live News for {ticker} via Finnhub...")
        
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        try:
            news = self.client.company_news(ticker, _from=start_date, to=end_date)
            return [{"headline": n['headline'], "summary": n['summary']} for n in news[:3]]
        except Exception as e:
            return [{"headline": "News API Error", "summary": str(e)}]