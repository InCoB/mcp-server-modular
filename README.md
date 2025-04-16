# MCP Demo Server

Running 

masteraccount@Mac Server % cd mcp-server-demo
masteraccount@Mac mcp-server-demo % export PYTHONPATH=$PWD/src
uv run mcp dev src/mcp_demo/server.py
     

A modular Model Context Protocol (MCP) server that demonstrates best practices for building MCP applications.

## Project Structure

```
mcp-demo/
├── src/
│   └── mcp_demo/           # Main package
│       ├── config/        # Configuration settings
│       ├── resources/     # MCP resources
│       ├── tools/        # MCP tools by domain
│       ├── utils/        # Shared utilities
│       ├── __init__.py   # Package initialization
│       └── server.py     # Main server entry point
├── pyproject.toml        # Project configuration and dependencies
└── README.md            # This file
```

## Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mcp-demo.git
   cd mcp-demo
   ```

2. Install the package and dependencies:
   ```bash
   uv pip install .
   ```

## Running the Server

You can run the server using `uv`:

```bash
uv run src/mcp_demo/server.py
```

## Development

To install in development mode:

```bash
uv pip install -e .
```

## Features

- Modular architecture with clear separation of concerns
- Type-safe implementation
- Comprehensive error handling
- Security-first approach
- Easy to extend with new tools and resources

## Documentation

For detailed documentation on:
- [Adding Tools](docs/guides/adding-tools.md)
- [Adding Resources](docs/guides/adding-resources.md)
- [Configuration Management](docs/guides/configuration.md)

## License

MIT
