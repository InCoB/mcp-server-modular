from typing import Dict, Any, Optional, Union
from mcp.server.fastmcp import FastMCP
from mcp_demo.utils.http import make_http_request

def register_http_tools(mcp: FastMCP) -> None:
    """Register all HTTP-related tools."""
    
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
        return make_http_request(
            url=url,
            method=method,
            headers=headers,
            params=params,
            data=data,
            json_body=json_body,
            timeout=timeout
        ) 