#!/usr/bin/env python3

"""
Calendar MCP Server
Provides calendar integration capabilities for MCP clients.
Uses basic MCP server with custom HTTP wrapper for Render deployment
"""

import os
import sys
import asyncio
from datetime import datetime, timedelta
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create MCP server with basic server for full control
server = Server("Calendar MCP Server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="get_current_date",
            description="Get the current date and time",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_today",
            description="Get today's date",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_yesterday",
            description="Get yesterday's date",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_tomorrow",
            description="Get tomorrow's date",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_date_info",
            description="Get information about a specific date",
            inputSchema={
                "type": "object",
                "properties": {
                    "date_string": {"type": "string", "description": "Date in YYYY-MM-DD format"}
                },
                "required": ["date_string"]
            }
        ),
        Tool(
            name="add_days_to_date",
            description="Add or subtract days from a given date",
            inputSchema={
                "type": "object",
                "properties": {
                    "date_string": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                    "days": {"type": "integer", "description": "Number of days to add (negative to subtract)"}
                },
                "required": ["date_string", "days"]
            }
        ),
        Tool(
            name="get_days_between_dates",
            description="Calculate the number of days between two dates",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_date": {"type": "string", "description": "Start date in YYYY-MM-DD format"},
                    "end_date": {"type": "string", "description": "End date in YYYY-MM-DD format"}
                },
                "required": ["start_date", "end_date"]
            }
        ),
        Tool(
            name="schedule_reminder",
            description="Schedule a calendar reminder",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the reminder"},
                    "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                    "time": {"type": "string", "description": "Time in HH:MM format"}
                },
                "required": ["title", "date", "time"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls"""
    if name == "get_current_date":
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return [TextContent(type="text", text=current_time)]
    
    elif name == "get_today":
        today = datetime.now().strftime("%Y-%m-%d")
        return [TextContent(type="text", text=today)]
    
    elif name == "get_yesterday":
        yesterday = datetime.now() - timedelta(days=1)  # Fixed: was incorrectly adding days
        return [TextContent(type="text", text=yesterday.strftime("%Y-%m-%d"))]
    
    elif name == "get_tomorrow":
        tomorrow = datetime.now() + timedelta(days=1)
        return [TextContent(type="text", text=tomorrow.strftime("%Y-%m-%d"))]
    
    elif name == "get_date_info":
        date_string = arguments.get("date_string", "")
        try:
            date_obj = datetime.strptime(date_string, "%Y-%m-%d")
            day_of_week = date_obj.strftime("%A")
            month_name = date_obj.strftime("%B")
            day = date_obj.day
            year = date_obj.year
            
            result = f"Date: {date_string}, Day: {day_of_week}, Month: {month_name}, Day: {day}, Year: {year}"
            return [TextContent(type="text", text=result)]
        except ValueError:
            return [TextContent(type="text", text=f"Invalid date format: {date_string}. Please use YYYY-MM-DD format.")]
    
    elif name == "add_days_to_date":
        date_string = arguments.get("date_string", "")
        days = arguments.get("days", 0)
        try:
            date_obj = datetime.strptime(date_string, "%Y-%m-%d")
            new_date = date_obj + timedelta(days=days)
            return [TextContent(type="text", text=new_date.strftime("%Y-%m-%d"))]
        except ValueError:
            return [TextContent(type="text", text=f"Invalid date format: {date_string}. Please use YYYY-MM-DD format.")]
    
    elif name == "get_days_between_dates":
        start_date = arguments.get("start_date", "")
        end_date = arguments.get("end_date", "")
        try:
            start_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_obj = datetime.strptime(end_date, "%Y-%m-%d")
            diff = end_obj - start_obj
            return [TextContent(type="text", text=f"Days between {start_date} and {end_date}: {diff.days}")]
        except ValueError:
            return [TextContent(type="text", text="Invalid date format. Please use YYYY-MM-DD format for both dates.")]
    
    elif name == "schedule_reminder":
        title = arguments.get("title", "")
        date = arguments.get("date", "")
        time = arguments.get("time", "")
        
        try:
            # Validate date and time format
            datetime.strptime(date, "%Y-%m-%d")
            datetime.strptime(time, "%H:%M")
            
            # In a real implementation, this would integrate with actual calendar APIs
            result = f"Reminder scheduled: '{title}' on {date} at {time}"
            return [TextContent(type="text", text=result)]
        except ValueError:
            return [TextContent(type="text", text="Invalid date or time format. Use YYYY-MM-DD for date and HH:MM for time.")]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Main entry point"""
    port = int(os.getenv("PORT", "8000"))
    
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        # Run with stdio transport for local development
        print("🔧 Running Calendar MCP Server with stdio transport", file=sys.stderr)
        async with stdio_server() as streams:
            await server.run(streams[0], streams[1])
    else:
        # Run with SSE transport for n8n MCP Client compatibility
        print(f"🚀 Starting Calendar MCP Server with SSE transport on port {port}", file=sys.stderr)
        print(f"📡 MCP SSE endpoint: http://0.0.0.0:{port}/sse", file=sys.stderr)
        print(f"❤️  Health check endpoint: http://0.0.0.0:{port}/", file=sys.stderr)
        print(f"🌍 Environment: {os.getenv('RENDER', 'local')}", file=sys.stderr)
        
        # Import SSE transport
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Route
        from starlette.responses import JSONResponse
        import uvicorn
        
        # Create SSE transport
        sse = SseServerTransport("/messages")
        
        async def health_check(request):
            return JSONResponse({
                "status": "healthy",
                "service": "Calendar MCP Server",
                "version": "1.0.0",
                "transport": "sse",
                "timestamp": datetime.now().isoformat()
            })
        
        # Create Starlette app with SSE support
        app = Starlette(routes=[
            Route("/", health_check),
            Route("/health", health_check),
        ])
        
        # Add SSE routes
        sse.add_routes(app, server)
        
        print(f"📡 Calendar MCP Server running with SSE on http://0.0.0.0:{port}", file=sys.stderr)
        print("🏃 Server is running. Press Ctrl+C to stop.", file=sys.stderr)
        
        # Run with uvicorn
        config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
        server_instance = uvicorn.Server(config)
        await server_instance.serve()

if __name__ == "__main__":
    asyncio.run(main())