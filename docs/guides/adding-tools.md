# Adding Tools to MCP Server

This guide explains how to add new tools to the MCP server. Tools are functions that can be called by LLMs to perform actions or retrieve data.

## Table of Contents
1. [Tool Structure](#tool-structure)
2. [Creating a New Tool](#creating-a-new-tool)
3. [Tool Categories](#tool-categories)
4. [Best Practices](#best-practices)
5. [Examples](#examples)

## Tool Structure

Each tool consists of:
1. A function decorated with `@mcp.tool()`
2. Type hints for parameters and return value
3. Docstring describing functionality
4. Error handling
5. Registration in the server

### Basic Tool Template

```python
from typing import Any, Dict
from mcp.server.fastmcp import FastMCP

def register_my_tools(mcp: FastMCP) -> None:
    """Register all tools in this category."""
    
    @mcp.tool()
    def my_tool(param1: str, param2: int = 0) -> Dict[str, Any]:
        """
        Description of what the tool does.
        
        Args:
            param1: Description of param1
            param2: Description of param2 (optional)
            
        Returns:
            Dictionary containing the result
        """
        try:
            # Tool implementation
            result = do_something(param1, param2)
            return {
                "error": False,
                "data": result
            }
        except Exception as e:
            return {
                "error": True,
                "message": str(e)
            }
```

## Creating a New Tool

1. **Choose Category**
   - Determine which existing category fits your tool
   - Or create a new category if needed

2. **Create/Update File**
   ```python
   # tools/my_category.py
   from mcp.server.fastmcp import FastMCP
   
   def register_my_category_tools(mcp: FastMCP) -> None:
       # Tool definitions here
   ```

3. **Register in Server**
   ```python
   # server.py
   from tools.my_category import register_my_category_tools
   
   def create_server():
       mcp = FastMCP("Demo")
       register_my_category_tools(mcp)
       return mcp
   ```

## Tool Categories

Tools should be organized by domain:

1. **Data Operations**
   - Database queries
   - File operations
   - Data transformation

2. **External Services**
   - API calls
   - Web requests
   - Third-party integrations

3. **System Operations**
   - Process management
   - System information
   - Resource monitoring

4. **Domain-Specific**
   - Finance (stock prices, calculations)
   - Math (computations, statistics)
   - Text processing

## Best Practices

1. **Type Safety**
   ```python
   def my_tool(
       required_param: str,
       optional_param: Optional[int] = None
   ) -> Dict[str, Any]:
   ```

2. **Documentation**
   ```python
   @mcp.tool()
   def my_tool(param: str) -> str:
       """
       Clear description of the tool.
       
       Args:
           param: What this parameter does
           
       Returns:
           Description of return value
           
       Raises:
           ValueError: When param is invalid
       """
   ```

3. **Error Handling**
   ```python
   try:
       result = process_data(param)
       return {"error": False, "data": result}
   except ValueError as e:
       return {"error": True, "message": f"Invalid input: {e}"}
   except Exception as e:
       return {"error": True, "message": f"Unexpected error: {e}"}
   ```

4. **Input Validation**
   ```python
   def my_tool(value: int) -> Dict[str, Any]:
       if not 0 <= value <= 100:
           return {
               "error": True,
               "message": "Value must be between 0 and 100"
           }
   ```

5. **Use Utils**
   ```python
   from ..utils.http import make_http_request
   
   @mcp.tool()
   def fetch_data(url: str) -> Dict[str, Any]:
       return make_http_request(url)
   ```

## Examples

### 1. Simple Math Tool
```python
@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b
```

### 2. API Tool
```python
@mcp.tool()
def get_weather(city: str) -> Dict[str, Any]:
    """Get weather for a city."""
    url = f"https://api.weather.com/{city}"
    return make_http_request(url)
```

### 3. Data Processing Tool
```python
@mcp.tool()
def analyze_text(text: str) -> Dict[str, Any]:
    """Analyze text statistics."""
    return {
        "error": False,
        "data": {
            "length": len(text),
            "words": len(text.split()),
            "lines": len(text.splitlines())
        }
    }
```

### 4. Complex Tool with Multiple Parameters
```python
@mcp.tool()
def filter_data(
    data: List[Dict[str, Any]],
    field: str,
    value: Any,
    case_sensitive: bool = True
) -> Dict[str, Any]:
    """Filter a list of dictionaries by field value."""
    try:
        if not case_sensitive and isinstance(value, str):
            filtered = [
                item for item in data
                if str(item.get(field)).lower() == value.lower()
            ]
        else:
            filtered = [
                item for item in data
                if item.get(field) == value
            ]
        
        return {
            "error": False,
            "data": filtered,
            "count": len(filtered)
        }
    except Exception as e:
        return {
            "error": True,
            "message": f"Error filtering data: {e}"
        }
``` 