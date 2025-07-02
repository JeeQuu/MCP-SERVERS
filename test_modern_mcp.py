#!/usr/bin/env python3

"""
Test modern MCP server using built-in Streamable HTTP transport
This demonstrates the current SDK v1.10.1 capabilities
"""

import os
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

# Create MCP server with built-in Streamable HTTP support
mcp = FastMCP("Test Modern MCP Server")

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@mcp.tool()
def get_env_var(name: str) -> str:
    """Get an environment variable value"""
    return os.getenv(name, "Not found")

@mcp.resource("config://server")
def get_config() -> str:
    """Get server configuration"""
    return "Modern MCP Server Configuration"

if __name__ == "__main__":
    # Run with modern Streamable HTTP transport
    print("🚀 Starting Modern MCP Server with Streamable HTTP on port 8000")
    print("📡 Streamable HTTP endpoint: http://localhost:8000/mcp")
    print("❤️  Health check endpoint: http://localhost:8000/")
    mcp.run(transport="streamable-http") 