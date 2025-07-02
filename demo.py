#!/usr/bin/env python3
"""
Demo script showing multi-client MCP server usage
"""

import asyncio
import os
from config_manager import set_client

# Simulated MCP server usage
class DemoMCPUsage:
    def __init__(self):
        pass
    
    async def demo_client_switching(self):
        """Demonstrate switching between clients"""
        
        print("🎯 Multi-Client MCP Server Demo")
        print("=" * 50)
        
        # Client 1: Personal use
        print("\n📱 Switching to 'personal' client...")
        config1 = set_client("personal")
        print(f"Client ID: {config1.client_id}")
        print(f"Gmail token path: {config1.get('gmail', 'token_path')}")
        print(f"Telegram config: {config1.get('telegram', 'chat_id', 'Not configured')}")
        
        # Client 2: Business client
        print("\n🏢 Switching to 'acme_corp' client...")
        config2 = set_client("acme_corp")
        print(f"Client ID: {config2.client_id}")
        print(f"Gmail token path: {config2.get('gmail', 'token_path')}")
        print(f"Business hours: {config2.get('calendar', 'business_hours', 'Not configured')}")
        
        # Client 3: Agency client
        print("\n🎨 Switching to 'design_agency' client...")
        config3 = set_client("design_agency")
        print(f"Client ID: {config3.client_id}")
        print(f"Supabase table prefix: {config3.get('supabase', 'table_prefix', 'Not configured')}")
        
        print("\n✨ Each client has completely isolated:")
        print("   - Credentials & API keys")
        print("   - Configuration settings")
        print("   - Token storage")
        print("   - Business logic preferences")
    
    async def demo_workflow_example(self):
        """Show how this works in a real workflow"""
        
        print("\n🔄 Workflow Example: Client-Specific Email Processing")
        print("=" * 60)
        
        # Simulate different clients with different workflows
        clients = [
            {
                "id": "tech_startup",
                "name": "Tech Startup",
                "workflow": "Process support emails → Create tickets → Notify Slack"
            },
            {
                "id": "law_firm", 
                "name": "Law Firm",
                "workflow": "Process contracts → Extract dates → Calendar booking"
            },
            {
                "id": "marketing_agency",
                "name": "Marketing Agency", 
                "workflow": "Schedule content → Post to Instagram → Generate reports → Email clients"
            },
            {
                "id": "social_media_manager",
                "name": "Social Media Manager",
                "workflow": "Instagram analytics → PDF reports → Client dashboard → Performance alerts"
            },
            {
                "id": "tiktok_influencer",
                "name": "TikTok Influencer",
                "workflow": "TikTok trends → Content insights → Hashtag optimization → Performance tracking"
            }
        ]
        
        for client in clients:
            print(f"\n🏢 {client['name']} ({client['id']})")
            print(f"   Workflow: {client['workflow']}")
            
            # Simulate setting client context
            config = set_client(client['id'])
            
            # Show client-specific settings
            print(f"   Gmail path: credentials/{client['id']}/gmail_credentials.json")
            print(f"   Config file: configs/{client['id']}.yaml")
            print(f"   Timezone: {config.get('calendar', 'timezone', 'UTC')}")

def main():
    """Run the demo"""
    demo = DemoMCPUsage()
    
    print("🚀 Starting MCP Multi-Client Demo...")
    
    asyncio.run(demo.demo_client_switching())
    asyncio.run(demo.demo_workflow_example())
    
    print("\n🎉 Demo complete!")
    print("\nTo try this yourself:")
    print("1. python deploy_client.py --setup myclient --name 'My Company'")
    print("2. Edit configs/myclient.yaml with your API keys")
    print("3. python deploy_client.py --run myclient")
    print("4. Build awesome n8n workflows! 🔥")

if __name__ == "__main__":
    main() 