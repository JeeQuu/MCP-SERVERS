#!/usr/bin/env python3

"""
ElevenLabs MCP Server
Provides ElevenLabs Text-to-Speech integration capabilities for MCP clients.
Uses modern Streamable HTTP transport (built-in MCP SDK v1.10.1+)
"""

import os
import sys
import json
import base64
from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import FastMCP, Context
from dotenv import load_dotenv
import requests
import tempfile

# Load environment variables
load_dotenv()

# Create MCP server with modern Streamable HTTP support
mcp = FastMCP("ElevenLabs MCP Server")

def get_elevenlabs_config():
    """Get ElevenLabs API configuration"""
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set")
    
    return api_key

def get_elevenlabs_headers():
    """Get standard headers for ElevenLabs API requests"""
    api_key = get_elevenlabs_config()
    return {
        "Accept": "application/json",
        "xi-api-key": api_key
    }

@mcp.tool()
async def generate_speech(text: str, voice_id: str, ctx: Context, model_id: str = "eleven_monolingual_v1") -> str:
    """Generate speech from text using ElevenLabs TTS"""
    try:
        await ctx.info(f"Generating speech for text: {text[:50]}...")
        
        headers = get_elevenlabs_headers()
        headers["Content-Type"] = "application/json"
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        data = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            # Convert audio to base64
            audio_data = response.content
            base64_audio = base64.b64encode(audio_data).decode('utf-8')
            
            await ctx.info(f"Successfully generated speech: {len(audio_data)} bytes")
            
            result = f"""Speech Generation Results:
🎤 Text: {text[:100]}{'...' if len(text) > 100 else ''}
🎭 Voice ID: {voice_id}
🤖 Model: {model_id}
📁 Audio Size: {len(audio_data)} bytes
🎵 Format: MP3

📋 Base64 Audio Data (first 100 chars):
{base64_audio[:100]}...

💡 Use this base64 data to save the audio file as MP3."""
            
            return result
        else:
            error_data = response.json() if response.content else {}
            await ctx.error(f"Failed to generate speech: {error_data}")
            return f"Failed to generate speech: {error_data.get('detail', {}).get('message', 'Unknown error')}"
        
    except Exception as e:
        await ctx.error(f"Failed to generate speech: {str(e)}")
        return f"Failed to generate speech: {str(e)}"

@mcp.tool()
async def get_voices(ctx: Context) -> str:
    """Get list of available voices"""
    try:
        await ctx.info("Getting available voices")
        
        headers = get_elevenlabs_headers()
        url = "https://api.elevenlabs.io/v1/voices"
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            voices = data.get("voices", [])
            
            result = f"Available ElevenLabs Voices ({len(voices)} total):\n\n"
            
            for voice in voices:
                result += f"🎭 Voice: {voice.get('name', 'Unknown')}\n"
                result += f"   ID: {voice.get('voice_id', 'Unknown')}\n"
                result += f"   Category: {voice.get('category', 'Unknown')}\n"
                result += f"   Description: {voice.get('description', 'No description')[:100]}...\n"
                result += f"   Language: {', '.join(voice.get('labels', {}).keys()) if voice.get('labels') else 'Unknown'}\n\n"
            
            await ctx.info(f"Retrieved {len(voices)} voices")
            return result
        else:
            error_data = response.json() if response.content else {}
            await ctx.error(f"Failed to get voices: {error_data}")
            return f"Failed to get voices: {error_data.get('detail', {}).get('message', 'Unknown error')}"
        
    except Exception as e:
        await ctx.error(f"Failed to get voices: {str(e)}")
        return f"Failed to get voices: {str(e)}"

@mcp.tool()
async def get_voice_details(voice_id: str, ctx: Context) -> str:
    """Get detailed information about a specific voice"""
    try:
        await ctx.info(f"Getting details for voice: {voice_id}")
        
        headers = get_elevenlabs_headers()
        url = f"https://api.elevenlabs.io/v1/voices/{voice_id}"
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            voice = response.json()
            
            result = f"""Voice Details:
🎭 Name: {voice.get('name', 'Unknown')}
🔢 ID: {voice.get('voice_id', 'Unknown')}
📂 Category: {voice.get('category', 'Unknown')}
📝 Description: {voice.get('description', 'No description')}

⚙️ Settings:
• Stability: {voice.get('settings', {}).get('stability', 'N/A')}
• Similarity Boost: {voice.get('settings', {}).get('similarity_boost', 'N/A')}

🏷️ Labels:"""
            
            labels = voice.get('labels', {})
            if labels:
                for key, value in labels.items():
                    result += f"\n• {key}: {value}"
            else:
                result += "\n• No labels available"
            
            # Sample information
            samples = voice.get('samples', [])
            if samples:
                result += f"\n\n🎵 Samples: {len(samples)} available"
                for i, sample in enumerate(samples[:3], 1):  # Show first 3 samples
                    result += f"\n  {i}. {sample.get('file_name', f'Sample {i}')}"
            else:
                result += "\n\n🎵 Samples: None available"
            
            await ctx.info(f"Retrieved details for voice: {voice.get('name')}")
            return result
        else:
            error_data = response.json() if response.content else {}
            await ctx.error(f"Failed to get voice details: {error_data}")
            return f"Failed to get voice details: {error_data.get('detail', {}).get('message', 'Unknown error')}"
        
    except Exception as e:
        await ctx.error(f"Failed to get voice details: {str(e)}")
        return f"Failed to get voice details: {str(e)}"

@mcp.tool()
async def get_models(ctx: Context) -> str:
    """Get list of available TTS models"""
    try:
        await ctx.info("Getting available models")
        
        headers = get_elevenlabs_headers()
        url = "https://api.elevenlabs.io/v1/models"
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            models = data if isinstance(data, list) else data.get("models", [])
            
            result = f"Available ElevenLabs Models ({len(models)} total):\n\n"
            
            for model in models:
                result += f"🤖 Model: {model.get('name', 'Unknown')}\n"
                result += f"   ID: {model.get('model_id', 'Unknown')}\n"
                result += f"   Description: {model.get('description', 'No description')[:100]}...\n"
                result += f"   Languages: {', '.join(model.get('languages', [])) if model.get('languages') else 'Unknown'}\n\n"
            
            await ctx.info(f"Retrieved {len(models)} models")
            return result
        else:
            # Fallback with common models if API doesn't provide list
            result = """Available ElevenLabs Models (Common):

🤖 Model: Eleven Monolingual v1
   ID: eleven_monolingual_v1
   Description: English-only model with high quality
   Languages: English

🤖 Model: Eleven Multilingual v1
   ID: eleven_multilingual_v1
   Description: Supports multiple languages
   Languages: Multiple

🤖 Model: Eleven Multilingual v2
   ID: eleven_multilingual_v2
   Description: Enhanced multilingual model
   Languages: Multiple

🤖 Model: Eleven Turbo v2
   ID: eleven_turbo_v2
   Description: Fast generation with good quality
   Languages: Multiple

💡 Note: Use these model IDs when generating speech."""
            
            return result
        
    except Exception as e:
        await ctx.error(f"Failed to get models: {str(e)}")
        return f"Failed to get models: {str(e)}"

@mcp.tool()
async def get_user_info(ctx: Context) -> str:
    """Get user account information and quota"""
    try:
        await ctx.info("Getting user account information")
        
        headers = get_elevenlabs_headers()
        url = "https://api.elevenlabs.io/v1/user"
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            user = response.json()
            
            subscription = user.get('subscription', {})
            
            result = f"""ElevenLabs Account Information:
👤 User ID: {user.get('xi_api_key', 'Unknown')[:10]}...
💳 Subscription Tier: {subscription.get('tier', 'Unknown')}

📊 Usage Quota:
• Character Count: {subscription.get('character_count', 'Unknown')}
• Character Limit: {subscription.get('character_limit', 'Unknown')}
• Can Extend: {'Yes' if subscription.get('can_extend_character_limit') else 'No'}
• Can Use Instant Voice Cloning: {'Yes' if subscription.get('can_use_instant_voice_cloning') else 'No'}
• Can Use Professional Voice Cloning: {'Yes' if subscription.get('can_use_professional_voice_cloning') else 'No'}

📅 Subscription Status:
• Status: {subscription.get('status', 'Unknown')}
• Next Character Reset: {subscription.get('next_character_count_reset_unix', 'Unknown')}
• Voice Limit: {subscription.get('voice_limit', 'Unknown')}
• Professional Voice Limit: {subscription.get('professional_voice_limit', 'Unknown')}"""
            
            # Calculate usage percentage if data available
            char_count = subscription.get('character_count', 0)
            char_limit = subscription.get('character_limit', 0)
            if char_count and char_limit:
                usage_percent = (char_count / char_limit) * 100
                result += f"\n• Usage: {usage_percent:.1f}% ({char_count:,} / {char_limit:,} characters)"
            
            await ctx.info("Retrieved user account information")
            return result
        else:
            error_data = response.json() if response.content else {}
            await ctx.error(f"Failed to get user info: {error_data}")
            return f"Failed to get user info: {error_data.get('detail', {}).get('message', 'Unknown error')}"
        
    except Exception as e:
        await ctx.error(f"Failed to get user info: {str(e)}")
        return f"Failed to get user info: {str(e)}"

@mcp.tool()
async def generate_speech_with_settings(text: str, voice_id: str, ctx: Context, stability: float = 0.5, similarity_boost: float = 0.5, style: float = 0.0, use_speaker_boost: bool = True) -> str:
    """Generate speech with custom voice settings"""
    try:
        await ctx.info(f"Generating speech with custom settings for: {text[:50]}...")
        
        headers = get_elevenlabs_headers()
        headers["Content-Type"] = "application/json"
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost,
                "style": style,
                "use_speaker_boost": use_speaker_boost
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            # Convert audio to base64
            audio_data = response.content
            base64_audio = base64.b64encode(audio_data).decode('utf-8')
            
            await ctx.info(f"Successfully generated speech with custom settings: {len(audio_data)} bytes")
            
            result = f"""Custom Speech Generation Results:
🎤 Text: {text[:100]}{'...' if len(text) > 100 else ''}
🎭 Voice ID: {voice_id}
⚙️  Stability: {stability}
⚙️  Similarity Boost: {similarity_boost}
⚙️  Style: {style}
⚙️  Speaker Boost: {'Enabled' if use_speaker_boost else 'Disabled'}
📁 Audio Size: {len(audio_data)} bytes
🎵 Format: MP3

📋 Base64 Audio Data (first 100 chars):
{base64_audio[:100]}...

💡 Use this base64 data to save the audio file as MP3."""
            
            return result
        else:
            error_data = response.json() if response.content else {}
            await ctx.error(f"Failed to generate speech: {error_data}")
            return f"Failed to generate speech: {error_data.get('detail', {}).get('message', 'Unknown error')}"
        
    except Exception as e:
        await ctx.error(f"Failed to generate speech: {str(e)}")
        return f"Failed to generate speech: {str(e)}"

@mcp.tool()
async def get_pronunciation_dictionary(ctx: Context) -> str:
    """Get pronunciation dictionary for better text-to-speech"""
    try:
        await ctx.info("Getting pronunciation dictionary tips")
        
        # Since ElevenLabs doesn't have a direct pronunciation dictionary API,
        # provide helpful tips for better pronunciation
        
        result = """ElevenLabs Pronunciation Guide:

🗣️ **Phonetic Spelling Tips:**
• Use phonetic spelling for difficult words
• Example: "schedule" → "SHED-yool" or "SKED-yool"
• Example: "Worcester" → "WUS-ter"

📝 **SSML Support:**
• Use SSML tags for better control
• <break time="1s"/> - Add pauses
• <emphasis level="strong">word</emphasis> - Emphasize words
• <prosody rate="slow">text</prosody> - Control speed

🎭 **Voice-Specific Tips:**
• Different voices handle pronunciation differently
• Test with multiple voices for best results
• Professional voices often have better pronunciation

⚙️ **Settings for Better Pronunciation:**
• Higher stability (0.7-0.9) for consistent pronunciation
• Lower similarity boost (0.3-0.5) for clearer speech
• Use speaker boost for better clarity

🌍 **Multilingual Considerations:**
• Use multilingual models for non-English text
• Specify language context when mixing languages
• Consider voice language compatibility

💡 **Best Practices:**
• Write numbers as words: "123" → "one hundred twenty-three"
• Spell out abbreviations: "Dr." → "Doctor"
• Use punctuation for natural pauses
• Test and iterate for optimal results"""
        
        await ctx.info("Provided pronunciation dictionary tips")
        return result
        
    except Exception as e:
        await ctx.error(f"Failed to get pronunciation guide: {str(e)}")
        return f"Failed to get pronunciation guide: {str(e)}"

@mcp.resource("elevenlabs://account")
def get_elevenlabs_account() -> str:
    """Get ElevenLabs account resource"""
    try:
        api_key = get_elevenlabs_config()
        return f"ElevenLabs API Key: {'*' * 10}{api_key[-10:]}"
    except Exception as e:
        return f"Error accessing ElevenLabs account: {str(e)}"

@mcp.resource("elevenlabs://config")
def get_elevenlabs_config_resource() -> str:
    """Get ElevenLabs server configuration"""
    return """ElevenLabs MCP Server Configuration:
- Modern Streamable HTTP Transport ✅
- Text-to-Speech Generation ✅
- Voice Management ✅
- Model Selection ✅
- Custom Voice Settings ✅
- Account Information ✅
- Pronunciation Guide ✅
- Async Context Support ✅"""

def main():
    """Main entry point"""
    port = int(os.getenv("PORT", "8007"))
    
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        # Run with stdio transport for local development
        print("🔧 Running ElevenLabs MCP Server with stdio transport", file=sys.stderr)
        mcp.run(transport="stdio")
    else:
        # Run with modern Streamable HTTP transport for production
        print(f"🚀 Starting ElevenLabs MCP Server with Streamable HTTP on port {port}", file=sys.stderr)
        print(f"📡 Streamable HTTP endpoint: http://localhost:{port}/mcp", file=sys.stderr)
        print(f"❤️  Health check endpoint: http://localhost:{port}/", file=sys.stderr)
        
        # Configure for production deployment
        mcp.settings.host = "0.0.0.0"  # Accept connections from any host
        mcp.settings.port = port
        mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()