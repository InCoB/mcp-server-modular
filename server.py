from mcp.server.fastmcp import FastMCP 
import requests 
import json 
from typing import Dict, Any, Optional, Union  

# Create an MCP server 
mcp = FastMCP("Demo")  

# Add an addition tool 
@mcp.tool() 
def add(a: int, b: int) -> int:     
    """Add two numbers"""     
    return a + b  

# Add a dynamic greeting resource 
@mcp.resource("greeting://{name}") 
def get_greeting(name: str) -> str:     
    """Get a personalized greeting"""     
    return f"Hello, {name}!"  

# Add an HTTP request tool 
@mcp.tool() 
def http_request(     
    url: str,     
    method: str = "GET",     
    headers: Optional[Dict[str, str]] = None,     
    params: Optional[Dict[str, str]] = None,     
    data: Optional[Union[Dict[str, Any], str]] = None,     
    json_body: Optional[Dict[str, Any]] = None,     
    timeout: int = 30 
) -> Dict[str, Any]:     
    """     
    Make an HTTP request to a specified URL.          
    Args:         
        url: The URL to send the request to         
        method: HTTP method (GET, POST, PUT, DELETE, etc.)         
        headers: HTTP headers to include         
        params: Query parameters         
        data: Form data or request body         
        json_body: JSON data (will be converted to JSON)         
        timeout: Request timeout in seconds              
    Returns:         
        Dictionary containing response status, headers, and content     
    """     
    # Default headers if none provided     
    if headers is None:         
        headers = {}          
    
    # Security check - prevent requests to internal networks     
    blocked_hosts = ['localhost', '127.0.0.1', '0.0.0.0', '10.', '172.16.', '192.168.']     
    if any(host in url for host in blocked_hosts):         
        return {             
            "error": True,             
            "message": "Requests to internal networks are not allowed"         
        }          
    
    try:         
        # Make the HTTP request         
        response = requests.request(             
            method=method.upper(),             
            url=url,             
            headers=headers,             
            params=params,             
            data=data,             
            json=json_body,             
            timeout=timeout         
        )                  
        
        # Attempt to parse JSON response         
        try:             
            response_data = response.json()         
        except ValueError:             
            # If not JSON, return text content             
            response_data = response.text                  
        
        # Return structured response         
        return {             
            "status_code": response.status_code,             
            "headers": dict(response.headers),             
            "content": response_data,             
            "error": False         
        }          
    
    except Exception as e:         
        # Handle any errors         
        return {             
            "error": True,             
            "message": str(e)         
        }  

# Example for Yahoo Finance API 
@mcp.tool() 
def get_stock_price(symbol: str) -> Dict[str, Any]:     
    """     
    Get the current stock price for a given symbol using Yahoo Finance API.          
    Args:         
        symbol: Stock symbol (e.g., AAPL, MSFT, GOOG)              
    Returns:         
        Stock information including price     
    """     
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"     
    params = {         
        "interval": "1d",         
        "range": "1d"     
    }          
    
    # Use our http_request tool     
    response = http_request(url=url, params=params)          
    
    if response.get("error"):         
        return response          
    
    # Parse the Yahoo Finance response     
    try:         
        data = response["content"]
        
        # Check if content is a string (not properly parsed JSON)
        if isinstance(data, str):
            return {
                "error": True,
                "message": f"Received non-JSON response: {data[:100]}..."
            }
            
        # Now safely access the nested data
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

# Run the server 
if __name__ == "__main__":     
    mcp.run()