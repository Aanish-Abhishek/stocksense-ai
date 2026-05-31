from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from ddgs import DDGS
import yfinance as yf

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

@tool
def get_stock_info(ticker: str) -> dict:
    """Fetches live stock price and key fundamentals for a given ticker."""
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "company_name":   info.get("longName", "N/A"),
        "current_price":  info.get("currentPrice", "N/A"),
        "previous_close": info.get("previousClose", "N/A"),
        "52w_high":       info.get("fiftyTwoWeekHigh", "N/A"),
        "52w_low":        info.get("fiftyTwoWeekLow", "N/A"),
        "pe_ratio":       info.get("trailingPE", "N/A"),
        "analyst_rating": info.get("recommendationKey", "N/A"),
    }

@tool
def fetch_news(company_name: str) -> str:
    """Fetches latest news for a given company."""
    with DDGS() as ddgs:
        results = list(ddgs.news(
            query=f"{company_name} stock news",
            max_results=5
        ))
    formatted = ""
    for i, item in enumerate(results):
        formatted += f"{i+1}. {item['title']}\n   {item['body']}\n\n"
    return formatted

tools = [get_stock_info, fetch_news]

agent = create_agent(
    llm,
    tools,
    system_prompt=(
        "You are an expert stock research analyst. "
        "Always provide: "
        "1. Price Summary "
        "2. News Summary "
        "3. Sentiment: Bullish / Bearish / Neutral "
        "4. Signal: Buy / Hold / Sell with reasoning"
    ),
)