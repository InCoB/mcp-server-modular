import logging
from mcp.server.fastmcp import FastMCP
from mcp_demo.config.settings import SERVER_NAME, SERVER_VERSION
from mcp_demo.tools.math import register_math_tools
from mcp_demo.tools.http import register_http_tools
from mcp_demo.tools.finance import register_finance_tools
from mcp_demo.tools.web import register_web_tools
from mcp_demo.resources.greetings import register_greeting_resources

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def create_server() -> FastMCP:
    """Create and configure the MCP server."""
    logging.info("Creating MCP server...")
    mcp = FastMCP(SERVER_NAME, version=SERVER_VERSION)
    try:
        logging.info("Registering math tools...")
        register_math_tools(mcp)
        logging.info("Registering http tools...")
        register_http_tools(mcp)
        logging.info("Registering finance tools...")
        register_finance_tools(mcp)
        logging.info("Registering web tools...")
        register_web_tools(mcp)
        logging.info("Registering greeting resources...")
        register_greeting_resources(mcp)
        logging.info("All tools/resources registered successfully.")
    except Exception as e:
        logging.exception("Error during tool/resource registration: %s", e)
        raise
    return mcp

# Create the server instance globally
server = create_server()

if __name__ == "__main__":
    logging.info("Starting MCP server...")
    try:
        server.run()
    except Exception as e:
        logging.exception("Server crashed: %s", e)