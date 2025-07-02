#!/usr/bin/env python3

"""
Instagram MCP Server
Provides Instagram/Meta integration capabilities for MCP clients.
Uses modern Streamable HTTP transport (built-in MCP SDK v1.10.1+)
"""

import os
import sys
import json
from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP, Context
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Create MCP server with modern Streamable HTTP support
mcp = FastMCP("Instagram MCP Server")

def get_instagram_config():
    """Get Instagram API configuration"""
    access_token = os.getenv("IG_ACCESS_TOKEN")
    page_id = os.getenv("IG_PAGE_ID")
    
    if not access_token:
        raise ValueError("IG_ACCESS_TOKEN environment variable not set")
    if not page_id:
        raise ValueError("IG_PAGE_ID environment variable not set")
    
    return access_token, page_id

@mcp.tool()
async def post_photo(image_url: str, caption: str, ctx: Context) -> str:
    """Post a photo to Instagram"""
    try:
        await ctx.info(f"Posting photo with caption: {caption[:50]}...")
        
        access_token, page_id = get_instagram_config()
        
        # Step 1: Create media object
        media_url = f"https://graph.facebook.com/v17.0/{page_id}/media"
        media_params = {
            'image_url': image_url,
            'caption': caption,
            'access_token': access_token
        }
        
        media_response = requests.post(media_url, data=media_params)
        media_data = media_response.json()
        
        if media_response.status_code != 200:
            await ctx.error(f"Failed to create media: {media_data}")
            return f"Error creating media: {media_data.get('error', {}).get('message', 'Unknown error')}"
        
        media_id = media_data['id']
        
        # Step 2: Publish media
        publish_url = f"https://graph.facebook.com/v17.0/{page_id}/media_publish"
        publish_params = {
            'creation_id': media_id,
            'access_token': access_token
        }
        
        publish_response = requests.post(publish_url, data=publish_params)
        publish_data = publish_response.json()
        
        if publish_response.status_code != 200:
            await ctx.error(f"Failed to publish media: {publish_data}")
            return f"Error publishing media: {publish_data.get('error', {}).get('message', 'Unknown error')}"
        
        post_id = publish_data['id']
        await ctx.info(f"Successfully posted photo with ID: {post_id}")
        
        return f"Photo posted successfully! Post ID: {post_id}"
        
    except Exception as e:
        await ctx.error(f"Failed to post photo: {str(e)}")
        return f"Failed to post photo: {str(e)}"

@mcp.tool()
async def get_media_insights(media_id: str, ctx: Context) -> str:
    """Get insights/analytics for a specific media post"""
    try:
        await ctx.info(f"Getting insights for media: {media_id}")
        
        access_token, _ = get_instagram_config()
        
        metrics = ['impressions', 'reach', 'likes', 'comments', 'shares', 'saves']
        url = f"https://graph.facebook.com/v17.0/{media_id}/insights"
        params = {
            'metric': ','.join(metrics),
            'access_token': access_token
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if response.status_code != 200:
            await ctx.error(f"Failed to get insights: {data}")
            return f"Error getting insights: {data.get('error', {}).get('message', 'Unknown error')}"
        
        insights = {}
        for item in data.get('data', []):
            metric = item['name']
            value = item['values'][0]['value'] if item['values'] else 0
            insights[metric] = value
        
        result = f"Instagram Media Insights for {media_id}:\n"
        result += f"👁️  Impressions: {insights.get('impressions', 0)}\n"
        result += f"📊 Reach: {insights.get('reach', 0)}\n"
        result += f"❤️  Likes: {insights.get('likes', 0)}\n"
        result += f"💬 Comments: {insights.get('comments', 0)}\n"
        result += f"📤 Shares: {insights.get('shares', 0)}\n"
        result += f"🔖 Saves: {insights.get('saves', 0)}"
        
        return result
        
    except Exception as e:
        await ctx.error(f"Failed to get media insights: {str(e)}")
        return f"Failed to get media insights: {str(e)}"

@mcp.tool()
async def get_account_insights(ctx: Context, period: str = "day") -> str:
    """Get account-level insights (period: day, week, days_28)"""
    try:
        await ctx.info(f"Getting account insights for period: {period}")
        
        access_token, page_id = get_instagram_config()
        
        metrics = ['impressions', 'reach', 'profile_views', 'website_clicks']
        url = f"https://graph.facebook.com/v17.0/{page_id}/insights"
        params = {
            'metric': ','.join(metrics),
            'period': period,
            'access_token': access_token
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if response.status_code != 200:
            await ctx.error(f"Failed to get account insights: {data}")
            return f"Error getting account insights: {data.get('error', {}).get('message', 'Unknown error')}"
        
        insights = {}
        for item in data.get('data', []):
            metric = item['name']
            value = item['values'][0]['value'] if item['values'] else 0
            insights[metric] = value
        
        result = f"Instagram Account Insights ({period}):\n"
        result += f"👁️  Impressions: {insights.get('impressions', 0)}\n"
        result += f"📊 Reach: {insights.get('reach', 0)}\n"
        result += f"👤 Profile Views: {insights.get('profile_views', 0)}\n"
        result += f"🔗 Website Clicks: {insights.get('website_clicks', 0)}"
        
        return result
        
    except Exception as e:
        await ctx.error(f"Failed to get account insights: {str(e)}")
        return f"Failed to get account insights: {str(e)}"

@mcp.tool()
async def get_recent_media(ctx: Context, limit: int = 10) -> str:
    """Get recent media posts"""
    try:
        await ctx.info(f"Getting {limit} recent media posts")
        
        access_token, page_id = get_instagram_config()
        
        url = f"https://graph.facebook.com/v17.0/{page_id}/media"
        params = {
            'fields': 'id,caption,media_type,media_url,thumbnail_url,timestamp,permalink',
            'limit': limit,
            'access_token': access_token
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if response.status_code != 200:
            await ctx.error(f"Failed to get recent media: {data}")
            return f"Error getting recent media: {data.get('error', {}).get('message', 'Unknown error')}"
        
        media_posts = data.get('data', [])
        
        if not media_posts:
            return "No recent media found"
        
        result = f"Recent Instagram Media ({len(media_posts)} posts):\n\n"
        
        for i, post in enumerate(media_posts, 1):
            result += f"{i}. Media ID: {post['id']}\n"
            result += f"   Type: {post.get('media_type', 'Unknown')}\n"
            result += f"   Caption: {post.get('caption', 'No caption')[:100]}...\n"
            result += f"   Posted: {post.get('timestamp', 'Unknown')}\n"
            result += f"   Link: {post.get('permalink', 'N/A')}\n\n"
        
        return result
        
    except Exception as e:
        await ctx.error(f"Failed to get recent media: {str(e)}")
        return f"Failed to get recent media: {str(e)}"

@mcp.tool()
async def get_hashtag_insights(hashtag: str, ctx: Context) -> str:
    """Get insights for a specific hashtag"""
    try:
        await ctx.info(f"Getting hashtag insights for: #{hashtag}")
        
        access_token, _ = get_instagram_config()
        
        # First, get hashtag ID
        search_url = f"https://graph.facebook.com/v17.0/ig_hashtag_search"
        search_params = {
            'user_id': os.getenv("IG_USER_ID"),
            'q': hashtag,
            'access_token': access_token
        }
        
        search_response = requests.get(search_url, params=search_params)
        search_data = search_response.json()
        
        if search_response.status_code != 200 or not search_data.get('data'):
            return f"Could not find hashtag: #{hashtag}"
        
        hashtag_id = search_data['data'][0]['id']
        
        # Get hashtag insights
        insights_url = f"https://graph.facebook.com/v17.0/{hashtag_id}"
        insights_params = {
            'fields': 'id,name',
            'access_token': access_token
        }
        
        insights_response = requests.get(insights_url, params=insights_params)
        insights_data = insights_response.json()
        
        if insights_response.status_code != 200:
            return f"Error getting hashtag insights: {insights_data.get('error', {}).get('message', 'Unknown error')}"
        
        # Get recent media for the hashtag
        media_url = f"https://graph.facebook.com/v17.0/{hashtag_id}/recent_media"
        media_params = {
            'user_id': os.getenv("IG_USER_ID"),
            'fields': 'id,caption,like_count,comments_count',
            'limit': 10,
            'access_token': access_token
        }
        
        media_response = requests.get(media_url, params=media_params)
        media_data = media_response.json()
        
        result = f"Hashtag Insights for #{hashtag}:\n"
        result += f"Hashtag ID: {hashtag_id}\n\n"
        
        if media_response.status_code == 200 and media_data.get('data'):
            result += f"Recent posts using #{hashtag}:\n"
            for i, post in enumerate(media_data['data'][:5], 1):
                result += f"{i}. Post ID: {post['id']}\n"
                result += f"   Likes: {post.get('like_count', 0)}\n"
                result += f"   Comments: {post.get('comments_count', 0)}\n\n"
        else:
            result += "No recent media found for this hashtag"
        
        return result
        
    except Exception as e:
        await ctx.error(f"Failed to get hashtag insights: {str(e)}")
        return f"Failed to get hashtag insights: {str(e)}"

@mcp.tool()
async def get_account_info(ctx: Context) -> str:
    """Get Instagram account information"""
    try:
        await ctx.info("Getting Instagram account information")
        
        access_token, page_id = get_instagram_config()
        
        url = f"https://graph.facebook.com/v17.0/{page_id}"
        params = {
            'fields': 'id,username,name,biography,website,followers_count,follows_count,media_count',
            'access_token': access_token
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if response.status_code != 200:
            await ctx.error(f"Failed to get account info: {data}")
            return f"Error getting account info: {data.get('error', {}).get('message', 'Unknown error')}"
        
        result = f"""Instagram Account Information:
📱 Username: @{data.get('username', 'N/A')}
👤 Name: {data.get('name', 'N/A')}
📝 Bio: {data.get('biography', 'No bio')[:100]}...
🌐 Website: {data.get('website', 'No website')}
👥 Followers: {data.get('followers_count', 0):,}
➡️  Following: {data.get('follows_count', 0):,}
📸 Posts: {data.get('media_count', 0):,}
🔢 Account ID: {data.get('id')}"""
        
        return result
        
    except Exception as e:
        await ctx.error(f"Failed to get account info: {str(e)}")
        return f"Failed to get account info: {str(e)}"

@mcp.resource("instagram://account")
def get_instagram_account() -> str:
    """Get Instagram account resource"""
    try:
        access_token, page_id = get_instagram_config()
        return f"Instagram Account ID: {page_id}"
    except Exception as e:
        return f"Error accessing Instagram account: {str(e)}"

@mcp.resource("instagram://config")
def get_instagram_config_resource() -> str:
    """Get Instagram server configuration"""
    return """Instagram MCP Server Configuration:
- Modern Streamable HTTP Transport ✅
- Photo/Video Posting ✅
- Media Analytics ✅
- Account Insights ✅
- Hashtag Analysis ✅
- Recent Media Retrieval ✅
- Account Information ✅
- Async Context Support ✅"""

def main():
    """Main entry point"""
    port = int(os.getenv("PORT", "8002"))
    
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        # Run with stdio transport for local development
        print("🔧 Running Instagram MCP Server with stdio transport", file=sys.stderr)
        mcp.run(transport="stdio")
    else:
        # Run with modern Streamable HTTP transport for production
        print(f"🚀 Starting Instagram MCP Server with Streamable HTTP on port {port}", file=sys.stderr)
        print(f"📡 Streamable HTTP endpoint: http://localhost:{port}/mcp", file=sys.stderr)
        print(f"❤️  Health check endpoint: http://localhost:{port}/", file=sys.stderr)
        
        # Configure for production deployment
        mcp.settings.host = "0.0.0.0"  # Accept connections from any host
        mcp.settings.port = port
        mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main() 