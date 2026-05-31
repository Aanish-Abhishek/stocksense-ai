from fastapi import FastAPI
from agent import agent
from pydantic import BaseModel, Field
from typing import Annotated

class StockRequest(BaseModel):
    ticker: Annotated[str, Field(..., example="RELIANCE.NS", description="Stock ticker symbol to analyse")]

app = FastAPI()

@app.post("/analyse")
def analyse_stock(request: StockRequest):
    """Endpoint to analyse a stock ticker and return insights."""
    result = agent.invoke({
                "messages": [{
                    "role": "user",
                    "content": f"Analyse the stock {request.ticker.upper()}"
                }]
    })
    return result["messages"][-1].content