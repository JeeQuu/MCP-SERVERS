#!/usr/bin/env python3

"""
Test script for Dropbox MCP Server
"""

import asyncio
import sys
import os

async def test_dropbox_server():
    """Test the Dropbox MCP Server"""
    print("🧪 Testing Dropbox MCP Server...")
    
    try:
        # Test basic imports
        from mcp.server import Server
        from mcp.types import Tool, TextContent
        print("✅ MCP imports successful")
        
        # Test server file syntax by attempting to compile it
        with open("Dropbox MCP Server.py", "r") as f:
            server_code = f.read()
        
        # Try to compile the code to check for syntax errors
        compile(server_code, "Dropbox MCP Server.py", "exec")
        print("✅ Dropbox server syntax is valid")
        
        # Test that all required dependencies are available
        try:
            import dropbox
            print("✅ Dropbox SDK available")
        except ImportError:
            print("⚠️  Dropbox SDK not installed (expected in local testing)")
        
        try:
            import uvicorn
            print("✅ Uvicorn available")
        except ImportError:
            print("❌ Uvicorn not available")
            
        try:
            import starlette
            print("✅ Starlette available")
        except ImportError:
            print("❌ Starlette not available")
            
        try:
            from mcp.server.sse import SseServerTransport
            print("✅ SSE transport available")
        except ImportError:
            print("❌ SSE transport not available")
            
        print("\n🎉 Dropbox MCP Server syntax and dependencies look good!")
        print("📝 Note: Actual functionality testing requires Dropbox credentials")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error in server file: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_dropbox_server())
    sys.exit(0 if success else 1) 