from mcp.server.fastmcp import FastMCP

def register_greeting_resources(mcp: FastMCP) -> None:
    """Register all greeting-related resources."""
    
    @mcp.resource("greeting://{name}")
    def get_greeting(name: str) -> str:
        """Get a personalized greeting."""
        return f"Hello, {name}!" 