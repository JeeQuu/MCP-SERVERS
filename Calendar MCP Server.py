#!/usr/bin/env python3

"""
Calendar MCP Server
Provides calendar integration capabilities for MCP clients.
Uses modern Streamable HTTP transport (built-in MCP SDK v1.10.1+)
"""

import os
import sys
from datetime import datetime, timedelta
import asyncio
from typing import Optional
from mcp.server.fastmcp import FastMCP, Context
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create MCP server with modern Streamable HTTP support
mcp = FastMCP("Calendar MCP Server")

# Add explicit health check routes
@mcp.get("/")
async def health_check():
    """Health check endpoint for deployment services"""
    return {"status": "healthy", "service": "Calendar MCP Server", "version": "1.0.0"}

@mcp.get("/health")
async def health_check_detailed():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "service": "Calendar MCP Server",
        "version": "1.0.0",
        "transport": "streamable-http",
        "timestamp": datetime.now().isoformat()
    }

@mcp.tool()
def get_current_date() -> str:
    """Get the current date and time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@mcp.tool()
def get_today() -> str:
    """Get today's date"""
    return datetime.now().strftime("%Y-%m-%d")

@mcp.tool()
def get_yesterday() -> str:
    """Get yesterday's date"""
    yesterday = datetime.now() - timedelta(days=1)  # Fixed: was incorrectly adding days
    return yesterday.strftime("%Y-%m-%d")

@mcp.tool()
def get_tomorrow() -> str:
    """Get tomorrow's date"""
    tomorrow = datetime.now() + timedelta(days=1)
    return tomorrow.strftime("%Y-%m-%d")

@mcp.tool()
def get_date_info(date_string: str) -> str:
    """Get information about a specific date"""
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d")
        day_of_week = date_obj.strftime("%A")
        month_name = date_obj.strftime("%B")
        day = date_obj.day
        year = date_obj.year
        
        return f"Date: {date_string}, Day: {day_of_week}, Month: {month_name}, Day: {day}, Year: {year}"
    except ValueError:
        return f"Invalid date format: {date_string}. Please use YYYY-MM-DD format."

@mcp.tool()
def add_days_to_date(date_string: str, days: int) -> str:
    """Add or subtract days from a given date"""
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d")
        new_date = date_obj + timedelta(days=days)
        return new_date.strftime("%Y-%m-%d")
    except ValueError:
        return f"Invalid date format: {date_string}. Please use YYYY-MM-DD format."

@mcp.tool()
def get_days_between_dates(start_date: str, end_date: str) -> str:
    """Calculate the number of days between two dates"""
    try:
        start_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_obj = datetime.strptime(end_date, "%Y-%m-%d")
        diff = end_obj - start_obj
        return f"Days between {start_date} and {end_date}: {diff.days}"
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD format for both dates."

@mcp.tool()
async def schedule_reminder(title: str, date: str, time: str, ctx: Context) -> str:
    """Schedule a calendar reminder"""
    try:
        # Validate date and time format
        datetime.strptime(date, "%Y-%m-%d")
        datetime.strptime(time, "%H:%M")
        
        await ctx.info(f"Scheduling reminder: {title} on {date} at {time}")
        
        # In a real implementation, this would integrate with actual calendar APIs
        return f"Reminder scheduled: '{title}' on {date} at {time}"
    except ValueError:
        return "Invalid date or time format. Use YYYY-MM-DD for date and HH:MM for time."

@mcp.resource("calendar://events/today")
def get_todays_events() -> str:
    """Get today's calendar events"""
    today = datetime.now().strftime("%Y-%m-%d")
    return f"Calendar events for {today}: [This would show actual events from calendar API]"

@mcp.resource("calendar://config")
def get_calendar_config() -> str:
    """Get calendar server configuration"""
    return """Calendar MCP Server Configuration:
- Modern Streamable HTTP Transport ✅
- Date/Time Operations ✅
- Calendar Integration Ready ✅
- Async Context Support ✅"""

def main():
    """Main entry point"""
    port = int(os.getenv("PORT", "8000"))
    
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        # Run with stdio transport for local development
        print("🔧 Running Calendar MCP Server with stdio transport", file=sys.stderr)
        mcp.run(transport="stdio")
    else:
        # Run with modern Streamable HTTP transport for production
        print(f"🚀 Starting Calendar MCP Server with Streamable HTTP on port {port}", file=sys.stderr)
        print(f"📡 Streamable HTTP endpoint: http://localhost:{port}/mcp", file=sys.stderr)
        print(f"❤️  Health check endpoint: http://localhost:{port}/", file=sys.stderr)
        
        # Configure for production deployment
        mcp.settings.host = "0.0.0.0"  # Accept connections from any host
        mcp.settings.port = port
        mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()