#!/usr/bin/env python3
"""
Calendar MCP Server - Render Deployment Entry Point
Modern Streamable HTTP Transport for n8n Integration
"""

import subprocess
import sys
import os

def main():
    # Ensure we're in the right directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("🚀 Starting Calendar MCP Server for Render deployment...")
    print("📡 This will be accessible for n8n integration")
    
    # Start the Calendar MCP Server
    try:
        subprocess.run([sys.executable, "Calendar MCP Server.py"], check=True)
    except KeyboardInterrupt:
        print("✅ Calendar MCP Server stopped gracefully")
    except Exception as e:
        print(f"❌ Error starting Calendar MCP Server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 