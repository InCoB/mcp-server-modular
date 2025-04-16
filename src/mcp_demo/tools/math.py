from mcp.server.fastmcp import FastMCP

def register_math_tools(mcp: FastMCP) -> None:
    """Register all math-related tools."""
    
    @mcp.tool()
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b 