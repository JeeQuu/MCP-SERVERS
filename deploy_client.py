#!/usr/bin/env python3
"""
Client Deployment Script for MCP Servers
"""

import os
import sys
import argparse
from pathlib import Path
from config_manager import ConfigManager

def setup_new_client(client_id: str, client_name: str = None):
    """Set up configuration and directories for a new client"""
    
    print(f"🔧 Setting up client: {client_id}")
    
    # Create config manager and template
    config_manager = ConfigManager()
    config_file = config_manager.create_client_config_template(client_id)
    
    print(f"✅ Created configuration template: {config_file}")
    print(f"📁 Created directories:")
    print(f"   - credentials/{client_id}/")
    print(f"   - tokens/{client_id}/")
    
    # Create client-specific scripts
    create_deployment_scripts(client_id)
    
    print(f"\n📋 Next steps for client '{client_id}':")
    print(f"1. Edit the configuration file: {config_file}")
    print(f"2. Add Gmail credentials to: credentials/{client_id}/gmail_credentials.json")
    print(f"3. Update API keys in the config file")
    print(f"4. Run: python deploy_client.py --run {client_id}")

def create_deployment_scripts(client_id: str):
    """Create client-specific deployment scripts"""
    
    # Docker compose file
    docker_compose = f"""version: '3.8'

services:
  mcp-gmail-{client_id}:
    build: .
    environment:
      - MCP_CLIENT_ID={client_id}
    volumes:
      - ./configs:/app/configs
      - ./credentials:/app/credentials
      - ./tokens:/app/tokens
    restart: unless-stopped
    
  mcp-telegram-{client_id}:
    build: .
    environment:
      - MCP_CLIENT_ID={client_id}
    volumes:
      - ./configs:/app/configs
    restart: unless-stopped
    
  mcp-pdf-{client_id}:
    build: .
    environment:
      - MCP_CLIENT_ID={client_id}
    volumes:
      - ./configs:/app/configs
    restart: unless-stopped
    
  mcp-instagram-{client_id}:
    build: .
    environment:
      - MCP_CLIENT_ID={client_id}
    volumes:
      - ./configs:/app/configs
    restart: unless-stopped
    
  mcp-tiktok-{client_id}:
    build: .
    environment:
      - MCP_CLIENT_ID={client_id}
    volumes:
      - ./configs:/app/configs
    restart: unless-stopped
"""
    
    Path(f"deployments/{client_id}").mkdir(parents=True, exist_ok=True)
    
    with open(f"deployments/{client_id}/docker-compose.yml", 'w') as f:
        f.write(docker_compose)
    
    # Environment file
    env_file = f"""# Environment variables for client: {client_id}
MCP_CLIENT_ID={client_id}

# Override specific configs if needed
# {client_id.upper()}_GMAIL_CREDENTIALS_PATH=custom/path
# {client_id.upper()}_TELEGRAM_TOKEN=custom_token
"""
    
    with open(f"deployments/{client_id}/.env", 'w') as f:
        f.write(env_file)
    
    # Start script
    start_script = f"""#!/bin/bash
# Start MCP servers for client: {client_id}

export MCP_CLIENT_ID={client_id}

echo "🚀 Starting MCP servers for client: {client_id}"

# Start each server in background
python "Gmail MPC Server.py" &
GMAIL_PID=$!

python "Telegram MPC Server.py" &
TELEGRAM_PID=$!

python "PDF Tools MPC Server.py" &
PDF_PID=$!

python "Calendar MPC Server.py" &
CALENDAR_PID=$!

python "Instagram MCP Server.py" &
INSTAGRAM_PID=$!

python "TikTok_MCP_Server.py" &
TIKTOK_PID=$!

echo "✅ Started servers with PIDs:"
echo "Gmail: $GMAIL_PID"
echo "Telegram: $TELEGRAM_PID" 
echo "PDF: $PDF_PID"
echo "Calendar: $CALENDAR_PID"
echo "Instagram: $INSTAGRAM_PID"
echo "TikTok: $TIKTOK_PID"

# Save PIDs for stopping later
echo "$GMAIL_PID" > deployments/{client_id}/gmail.pid
echo "$TELEGRAM_PID" > deployments/{client_id}/telegram.pid
echo "$PDF_PID" > deployments/{client_id}/pdf.pid
echo "$CALENDAR_PID" > deployments/{client_id}/calendar.pid
echo "$INSTAGRAM_PID" > deployments/{client_id}/instagram.pid
echo "$TIKTOK_PID" > deployments/{client_id}/tiktok.pid

echo "💡 To stop servers, run: python deploy_client.py --stop {client_id}"

wait
"""
    
    with open(f"deployments/{client_id}/start.sh", 'w') as f:
        f.write(start_script)
    
    os.chmod(f"deployments/{client_id}/start.sh", 0o755)

def run_client(client_id: str):
    """Run MCP servers for a specific client"""
    
    config_file = f"configs/{client_id}.yaml"
    if not os.path.exists(config_file):
        print(f"❌ Configuration not found: {config_file}")
        print(f"Run: python deploy_client.py --setup {client_id}")
        return
    
    print(f"🚀 Starting MCP servers for client: {client_id}")
    
    # Set environment
    os.environ["MCP_CLIENT_ID"] = client_id
    
    # Start the servers
    os.system(f"./deployments/{client_id}/start.sh")

def stop_client(client_id: str):
    """Stop MCP servers for a specific client"""
    
    print(f"🛑 Stopping MCP servers for client: {client_id}")
    
    pid_files = [
        f"deployments/{client_id}/gmail.pid",
        f"deployments/{client_id}/telegram.pid",
        f"deployments/{client_id}/pdf.pid",
        f"deployments/{client_id}/calendar.pid",
        f"deployments/{client_id}/instagram.pid",
        f"deployments/{client_id}/tiktok.pid"
    ]
    
    for pid_file in pid_files:
        if os.path.exists(pid_file):
            with open(pid_file, 'r') as f:
                pid = f.read().strip()
            try:
                os.kill(int(pid), 9)
                print(f"✅ Stopped process {pid}")
                os.remove(pid_file)
            except:
                print(f"⚠️  Could not stop process {pid}")

def list_clients():
    """List all configured clients"""
    
    configs_dir = Path("configs")
    if not configs_dir.exists():
        print("No clients configured yet")
        return
    
    print("📋 Configured clients:")
    for config_file in configs_dir.glob("*.yaml"):
        client_id = config_file.stem
        print(f"  - {client_id}")
        
        # Check if running
        pid_dir = Path(f"deployments/{client_id}")
        if pid_dir.exists() and any(pid_dir.glob("*.pid")):
            print(f"    Status: 🟢 Running")
        else:
            print(f"    Status: ⭕ Stopped")

def main():
    parser = argparse.ArgumentParser(description="Manage MCP server deployments for multiple clients")
    parser.add_argument("--setup", help="Set up a new client")
    parser.add_argument("--run", help="Run MCP servers for a client")
    parser.add_argument("--stop", help="Stop MCP servers for a client")
    parser.add_argument("--list", action="store_true", help="List all clients")
    parser.add_argument("--name", help="Client name (for setup)")
    
    args = parser.parse_args()
    
    if args.setup:
        setup_new_client(args.setup, args.name)
    elif args.run:
        run_client(args.run)
    elif args.stop:
        stop_client(args.stop)
    elif args.list:
        list_clients()
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 