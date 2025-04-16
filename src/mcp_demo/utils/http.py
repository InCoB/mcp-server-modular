from typing import Dict, Any, Optional, Union
import requests

def make_http_request(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, str]] = None,
    data: Optional[Union[Dict[str, Any], str]] = None,
    json_body: Optional[Dict[str, Any]] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """Make an HTTP request with security checks and error handling."""
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