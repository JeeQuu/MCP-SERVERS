#!/usr/bin/env python3

"""
Telegram MCP Server
Provides Telegram Bot integration capabilities for MCP clients.
Uses modern Streamable HTTP transport (built-in MCP SDK v1.10.1+)
"""

import os
import sys
import json
from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import FastMCP, Context
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Create MCP server with modern Streamable HTTP support
mcp = FastMCP("Telegram MCP Server")

def get_telegram_config():
    """Get Telegram Bot configuration"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    
    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
    
    return bot_token

def get_telegram_api_url(bot_token: str, method: str) -> str:
    """Get Telegram Bot API URL"""
    return f"https://api.telegram.org/bot{bot_token}/{method}"

@mcp.tool()
async def send_message(chat_id: str, text: str, ctx: Context, parse_mode: str = "HTML") -> str:
    """Send a message to a Telegram chat"""
    try:
        await ctx.info(f"Sending message to chat {chat_id}")
        
        bot_token = get_telegram_config()
        url = get_telegram_api_url(bot_token, "sendMessage")
        
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        
        response = requests.post(url, json=payload)
        data = response.json()
        
        if response.status_code == 200 and data.get("ok"):
            message_id = data["result"]["message_id"]
            await ctx.info(f"Message sent successfully with ID: {message_id}")
            return f"Message sent successfully! Message ID: {message_id}"
        else:
            await ctx.error(f"Failed to send message: {data}")
            return f"Failed to send message: {data.get('description', 'Unknown error')}"
        
    except Exception as e:
        await ctx.error(f"Failed to send message: {str(e)}")
        return f"Failed to send message: {str(e)}"

@mcp.tool()
async def send_photo(chat_id: str, photo_url: str, ctx: Context, caption: str = "") -> str:
    """Send a photo to a Telegram chat"""
    try:
        await ctx.info(f"Sending photo to chat {chat_id}")
        
        bot_token = get_telegram_config()
        url = get_telegram_api_url(bot_token, "sendPhoto")
        
        payload = {
            "chat_id": chat_id,
            "photo": photo_url,
            "caption": caption
        }
        
        response = requests.post(url, json=payload)
        data = response.json()
        
        if response.status_code == 200 and data.get("ok"):
            message_id = data["result"]["message_id"]
            await ctx.info(f"Photo sent successfully with ID: {message_id}")
            return f"Photo sent successfully! Message ID: {message_id}"
        else:
            await ctx.error(f"Failed to send photo: {data}")
            return f"Failed to send photo: {data.get('description', 'Unknown error')}"
        
    except Exception as e:
        await ctx.error(f"Failed to send photo: {str(e)}")
        return f"Failed to send photo: {str(e)}"

@mcp.tool()
async def get_updates(ctx: Context, limit: int = 10) -> str:
    """Get recent updates (messages) from the bot"""
    try:
        await ctx.info(f"Getting {limit} recent updates")
        
        bot_token = get_telegram_config()
        url = get_telegram_api_url(bot_token, "getUpdates")
        
        params = {
            "limit": limit,
            "timeout": 10
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if response.status_code == 200 and data.get("ok"):
            updates = data.get("result", [])
            
            if not updates:
                return "No recent updates found"
            
            result = f"Recent Telegram Updates ({len(updates)} messages):\n\n"
            
            for i, update in enumerate(updates, 1):
                message = update.get("message", {})
                chat = message.get("chat", {})
                from_user = message.get("from", {})
                
                result += f"{i}. Update ID: {update.get('update_id')}\n"
                result += f"   From: {from_user.get('first_name', 'Unknown')} (@{from_user.get('username', 'N/A')})\n"
                result += f"   Chat: {chat.get('title', chat.get('first_name', 'Unknown'))} (ID: {chat.get('id')})\n"
                result += f"   Text: {message.get('text', 'No text')[:100]}...\n"
                result += f"   Date: {message.get('date', 'Unknown')}\n\n"
            
            return result
        else:
            await ctx.error(f"Failed to get updates: {data}")
            return f"Failed to get updates: {data.get('description', 'Unknown error')}"
        
    except Exception as e:
        await ctx.error(f"Failed to get updates: {str(e)}")
        return f"Failed to get updates: {str(e)}"

@mcp.tool()
async def get_chat_info(chat_id: str, ctx: Context) -> str:
    """Get information about a chat"""
    try:
        await ctx.info(f"Getting info for chat {chat_id}")
        
        bot_token = get_telegram_config()
        url = get_telegram_api_url(bot_token, "getChat")
        
        params = {"chat_id": chat_id}
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if response.status_code == 200 and data.get("ok"):
            chat = data["result"]
            
            result = f"""Telegram Chat Information:
📱 Chat ID: {chat.get('id')}
🏷️  Type: {chat.get('type', 'Unknown')}
👤 Title/Name: {chat.get('title', chat.get('first_name', 'Unknown'))}
👥 Members Count: {chat.get('members_count', 'N/A')}
📝 Description: {chat.get('description', 'No description')[:100]}...
🔗 Username: @{chat.get('username', 'N/A')}
🖼️  Has Photo: {'Yes' if chat.get('photo') else 'No'}"""
            
            return result
        else:
            await ctx.error(f"Failed to get chat info: {data}")
            return f"Failed to get chat info: {data.get('description', 'Unknown error')}"
        
    except Exception as e:
        await ctx.error(f"Failed to get chat info: {str(e)}")
        return f"Failed to get chat info: {str(e)}"

@mcp.tool()
async def send_document(chat_id: str, document_url: str, ctx: Context, caption: str = "") -> str:
    """Send a document to a Telegram chat"""
    try:
        await ctx.info(f"Sending document to chat {chat_id}")
        
        bot_token = get_telegram_config()
        url = get_telegram_api_url(bot_token, "sendDocument")
        
        payload = {
            "chat_id": chat_id,
            "document": document_url,
            "caption": caption
        }
        
        response = requests.post(url, json=payload)
        data = response.json()
        
        if response.status_code == 200 and data.get("ok"):
            message_id = data["result"]["message_id"]
            await ctx.info(f"Document sent successfully with ID: {message_id}")
            return f"Document sent successfully! Message ID: {message_id}"
        else:
            await ctx.error(f"Failed to send document: {data}")
            return f"Failed to send document: {data.get('description', 'Unknown error')}"
        
    except Exception as e:
        await ctx.error(f"Failed to send document: {str(e)}")
        return f"Failed to send document: {str(e)}"

@mcp.tool()
async def set_webhook(webhook_url: str, ctx: Context) -> str:
    """Set webhook URL for the bot"""
    try:
        await ctx.info(f"Setting webhook to: {webhook_url}")
        
        bot_token = get_telegram_config()
        url = get_telegram_api_url(bot_token, "setWebhook")
        
        payload = {"url": webhook_url}
        
        response = requests.post(url, json=payload)
        data = response.json()
        
        if response.status_code == 200 and data.get("ok"):
            await ctx.info("Webhook set successfully")
            return f"Webhook set successfully to: {webhook_url}"
        else:
            await ctx.error(f"Failed to set webhook: {data}")
            return f"Failed to set webhook: {data.get('description', 'Unknown error')}"
        
    except Exception as e:
        await ctx.error(f"Failed to set webhook: {str(e)}")
        return f"Failed to set webhook: {str(e)}"

@mcp.tool()
async def get_bot_info(ctx: Context) -> str:
    """Get information about the bot"""
    try:
        await ctx.info("Getting bot information")
        
        bot_token = get_telegram_config()
        url = get_telegram_api_url(bot_token, "getMe")
        
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and data.get("ok"):
            bot = data["result"]
            
            result = f"""Telegram Bot Information:
🤖 Bot ID: {bot.get('id')}
👤 Name: {bot.get('first_name')} {bot.get('last_name', '')}
🔗 Username: @{bot.get('username')}
🗣️  Language: {bot.get('language_code', 'N/A')}
✅ Can Join Groups: {'Yes' if bot.get('can_join_groups') else 'No'}
📝 Can Read Messages: {'Yes' if bot.get('can_read_all_group_messages') else 'No'}
⚡ Supports Inline: {'Yes' if bot.get('supports_inline_queries') else 'No'}"""
            
            return result
        else:
            await ctx.error(f"Failed to get bot info: {data}")
            return f"Failed to get bot info: {data.get('description', 'Unknown error')}"
        
    except Exception as e:
        await ctx.error(f"Failed to get bot info: {str(e)}")
        return f"Failed to get bot info: {str(e)}"

@mcp.tool()
async def send_keyboard_message(chat_id: str, text: str, buttons: List[List[str]], ctx: Context) -> str:
    """Send a message with inline keyboard"""
    try:
        await ctx.info(f"Sending keyboard message to chat {chat_id}")
        
        bot_token = get_telegram_config()
        url = get_telegram_api_url(bot_token, "sendMessage")
        
        # Create inline keyboard
        keyboard = []
        for row in buttons:
            keyboard_row = []
            for button_text in row:
                keyboard_row.append({
                    "text": button_text,
                    "callback_data": button_text.lower().replace(" ", "_")
                })
            keyboard.append(keyboard_row)
        
        payload = {
            "chat_id": chat_id,
            "text": text,
            "reply_markup": {
                "inline_keyboard": keyboard
            }
        }
        
        response = requests.post(url, json=payload)
        data = response.json()
        
        if response.status_code == 200 and data.get("ok"):
            message_id = data["result"]["message_id"]
            await ctx.info(f"Keyboard message sent successfully with ID: {message_id}")
            return f"Keyboard message sent successfully! Message ID: {message_id}"
        else:
            await ctx.error(f"Failed to send keyboard message: {data}")
            return f"Failed to send keyboard message: {data.get('description', 'Unknown error')}"
        
    except Exception as e:
        await ctx.error(f"Failed to send keyboard message: {str(e)}")
        return f"Failed to send keyboard message: {str(e)}"

@mcp.resource("telegram://bot")
def get_telegram_bot() -> str:
    """Get Telegram bot resource"""
    try:
        bot_token = get_telegram_config()
        return f"Telegram Bot Token: {'*' * 10}{bot_token[-10:]}"
    except Exception as e:
        return f"Error accessing Telegram bot: {str(e)}"

@mcp.resource("telegram://config")
def get_telegram_config_resource() -> str:
    """Get Telegram server configuration"""
    return """Telegram MCP Server Configuration:
- Modern Streamable HTTP Transport ✅
- Message Sending ✅
- Photo/Document Sharing ✅
- Chat Information ✅
- Bot Management ✅
- Webhook Support ✅
- Inline Keyboards ✅
- Async Context Support ✅"""

def main():
    """Main entry point"""
    port = int(os.getenv("PORT", "8004"))
    
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        # Run with stdio transport for local development
        print("🔧 Running Telegram MCP Server with stdio transport", file=sys.stderr)
        mcp.run(transport="stdio")
    else:
        # Run with modern Streamable HTTP transport for production
        print(f"🚀 Starting Telegram MCP Server with Streamable HTTP on port {port}", file=sys.stderr)
        print(f"📡 Streamable HTTP endpoint: http://localhost:{port}/mcp", file=sys.stderr)
        print(f"❤️  Health check endpoint: http://localhost:{port}/", file=sys.stderr)
        
        # Configure for production deployment
        mcp.settings.host = "0.0.0.0"  # Accept connections from any host
        mcp.settings.port = port
        mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()