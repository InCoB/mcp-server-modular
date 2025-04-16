from typing import Dict, Any
from mcp.server.fastmcp import FastMCP
from ..utils.http import make_http_request
from ..config.settings import YAHOO_FINANCE_BASE_URL

def register_finance_tools(mcp: FastMCP) -> None:
    """Register all finance-related tools."""
    
    @mcp.tool()
    def get_stock_price(symbol: str) -> Dict[str, Any]:
        """
        Get the current stock price for a given symbol using Yahoo Finance API.
        
        Args:
            symbol: Stock symbol (e.g., AAPL, MSFT, GOOG)
            
        Returns:
            Stock information including price
        """
        url = f"{YAHOO_FINANCE_BASE_URL}/{symbol}"
        params = {
            "interval": "1d",
            "range": "1d"
        }
        
        response = make_http_request(url=url, params=params)
        
        if response.get("error"):
            return response
            
        try:
            data = response["content"]
            
            if isinstance(data, str):
                return {
                    "error": True,
                    "message": f"Received non-JSON response: {data[:100]}..."
                }
                
            if "chart" not in data:
                return {"error": True, "message": "No chart data in response"}
                
            chart_data = data["chart"]
            if "result" not in chart_data or not chart_data["result"]:
                return {"error": True, "message": "No result data in response"}
                
            result = chart_data["result"][0]
            if "meta" not in result:
                return {"error": True, "message": "No meta data in response"}
                
            meta = result["meta"]
            
            return {
                "symbol": symbol,
                "price": meta.get("regularMarketPrice"),
                "previous_close": meta.get("previousClose"),
                "currency": meta.get("currency"),
                "exchange": meta.get("exchangeName"),
                "error": False
            }
        except (KeyError, IndexError, TypeError) as e:
            return {
                "error": True,
                "message": f"Failed to parse Yahoo Finance data: {str(e)}"
            } 