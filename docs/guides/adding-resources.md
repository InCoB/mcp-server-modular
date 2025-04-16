# Adding Resources to MCP Server

This guide explains how to add new resources to the MCP server. Resources are data sources that can be accessed by LLMs through URI templates.

## Table of Contents
1. [Resource Structure](#resource-structure)
2. [Creating a New Resource](#creating-a-new-resource)
3. [Resource Types](#resource-types)
4. [Best Practices](#best-practices)
5. [Examples](#examples)

## Resource Structure

Each resource consists of:
1. A function decorated with `@mcp.resource(uri_template)`
2. URI template defining the resource path
3. Type hints for parameters and return value
4. Docstring describing the resource
5. Registration in the server

### Basic Resource Template

```python
from typing import Any, Dict
from mcp.server.fastmcp import FastMCP

def register_my_resources(mcp: FastMCP) -> None:
    """Register all resources in this category."""
    
    @mcp.resource("category://{param}")
    def my_resource(param: str) -> str:
        """
        Description of what the resource provides.
        
        Args:
            param: Description of the parameter
            
        Returns:
            The resource content
        """
        try:
            # Resource implementation
            return get_content(param)
        except Exception as e:
            return f"Error: {str(e)}"
```

## Creating a New Resource

1. **Choose Category**
   - Determine the appropriate category for your resource
   - Create a new category if needed

2. **Create/Update File**
   ```python
   # resources/my_category.py
   from mcp.server.fastmcp import FastMCP
   
   def register_my_category_resources(mcp: FastMCP) -> None:
       # Resource definitions here
   ```

3. **Register in Server**
   ```python
   # server.py
   from resources.my_category import register_my_category_resources
   
   def create_server():
       mcp = FastMCP("Demo")
       register_my_category_resources(mcp)
       return mcp
   ```

## Resource Types

Resources can provide different types of data:

1. **Text Resources**
   - Documentation
   - Configuration files
   - Log files
   - Source code

2. **Structured Data**
   - JSON objects
   - Database records
   - API responses
   - System information

3. **Binary Resources**
   - Images
   - PDFs
   - Audio files
   - Video files

4. **Dynamic Resources**
   - Real-time data
   - Computed values
   - Aggregated information

## Best Practices

1. **URI Templates**
   ```python
   # Simple parameter
   @mcp.resource("users://{user_id}")
   
   # Multiple parameters
   @mcp.resource("data://{type}/{id}")
   
   # Optional parameters
   @mcp.resource("logs://{date?}")
   
   # Query parameters
   @mcp.resource("search://{query}?page={page}&size={size}")
   ```

2. **Type Safety**
   ```python
   @mcp.resource("data://{id}")
   def get_data(id: int) -> Dict[str, Any]:
       """Get data by ID."""
       return fetch_data(id)
   ```

3. **Error Handling**
   ```python
   @mcp.resource("user://{id}")
   def get_user(id: str) -> str:
       try:
           user = find_user(id)
           return format_user(user)
       except UserNotFound:
           return f"User {id} not found"
       except Exception as e:
           return f"Error: {str(e)}"
   ```

4. **Documentation**
   ```python
   @mcp.resource("config://{section}")
   def get_config(section: str) -> str:
       """
       Get configuration settings for a section.
       
       Args:
           section: Configuration section name
           
       Returns:
           Configuration content as formatted text
           
       Example URI:
           config://database
           config://logging
       """
   ```

5. **Content Formatting**
   ```python
   def format_content(data: Dict[str, Any]) -> str:
       """Format data for consistent presentation."""
       return "\n".join(
           f"{key}: {value}"
           for key, value in data.items()
       )
   ```

## Examples

### 1. Simple Text Resource
```python
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting."""
    return f"Hello, {name}!"
```

### 2. Database Resource
```python
@mcp.resource("records://{table}/{id}")
def get_record(table: str, id: int) -> str:
    """Get a database record."""
    try:
        record = database.query(f"SELECT * FROM {table} WHERE id = ?", [id])
        return format_record(record)
    except Exception as e:
        return f"Error accessing {table}/{id}: {str(e)}"
```

### 3. Dynamic Resource
```python
@mcp.resource("stats://{metric}")
def get_stats(metric: str) -> str:
    """Get system statistics."""
    metrics = {
        "cpu": get_cpu_usage(),
        "memory": get_memory_usage(),
        "disk": get_disk_usage()
    }
    return f"{metric}: {metrics.get(metric, 'Unknown metric')}"
```

### 4. Complex Resource with Query Parameters
```python
@mcp.resource("search://{query}?page={page}&size={size}")
def search_content(
    query: str,
    page: int = 1,
    size: int = 10
) -> str:
    """
    Search content with pagination.
    
    Args:
        query: Search query
        page: Page number (default: 1)
        size: Results per page (default: 10)
    """
    try:
        results = perform_search(query, page, size)
        return format_search_results(results)
    except Exception as e:
        return f"Search error: {str(e)}"
```

### 5. Binary Resource
```python
from mcp.types import BinaryContent

@mcp.resource("images://{name}")
def get_image(name: str) -> BinaryContent:
    """Get an image file."""
    try:
        with open(f"images/{name}", "rb") as f:
            data = f.read()
        return BinaryContent(
            data=data,
            mime_type="image/jpeg"
        )
    except Exception as e:
        return BinaryContent(
            data=str(e).encode(),
            mime_type="text/plain"
        )
``` 