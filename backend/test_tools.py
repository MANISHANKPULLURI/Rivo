import asyncio
from tools.global_api import GlobalFinancials
from tools.indian_api import IndianFinancials
from tools.news_aggregator import FinancialNews
from tools.calculator import FinancialCalculator

async def run_verification():
    print("🔍 Starting Tool Verification for April 20, 2026...\n")

    # 1. Test Indian API
    india = IndianFinancials()
    rel_data = india.get_stock_data("RELIANCE")
    print(f"🇮🇳 Indian Market: Reliance is at {rel_data.get('current_price')} {rel_data.get('currency')}")

    # 2. Test Global API
    glob = GlobalFinancials()
    aapl_data = glob.get_stock_price("AAPL")
    print(f"🇺🇸 Global Market: Apple is at ${aapl_data.get('price')}")

    # 3. Test News Aggregator
    news = FinancialNews()
    latest = news.search_latest_news("Nifty 50 market today")
    print(f"📰 Latest News: Found {len(latest)} articles. Top: {latest[0]['title'] if latest else 'None'}")

    # 4. Test Calculator (Normalization & Accuracy)
    calc = FinancialCalculator()
    # Today's rate is approx 93.13 INR/USD
    usd_val = calc.convert_currency(rel_data.get('current_price', 0), 93.13)
    print(f"🧮 Math Check: Reliance price in USD: ${usd_val}")

if __name__ == "__main__":
    asyncio.run(run_verification())