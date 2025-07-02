#!/usr/bin/env python3
"""
Configuration Manager for Multi-Client MCP Servers
"""

import os
import json
import yaml
from typing import Dict, Any, Optional
from pathlib import Path

class ConfigManager:
    def __init__(self, client_id: Optional[str] = None):
        self.client_id = client_id or os.getenv("MCP_CLIENT_ID", "default")
        self.config_dir = Path("configs")
        self.config_dir.mkdir(exist_ok=True)
        
        # Load client-specific config
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration for the specified client"""
        
        # Try YAML first, then JSON, then environment variables
        config_file = self.config_dir / f"{self.client_id}.yaml"
        json_config_file = self.config_dir / f"{self.client_id}.json"
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        elif json_config_file.exists():
            with open(json_config_file, 'r') as f:
                return json.load(f)
        else:
            # Fall back to environment variables with client prefix
            return self._load_from_env()
    
    def _load_from_env(self) -> Dict[str, Any]:
        """Load config from environment variables with client prefix"""
        prefix = f"{self.client_id.upper()}_"
        
        config = {
            "gmail": {
                "credentials_path": os.getenv(f"{prefix}GMAIL_CREDENTIALS_PATH", 
                                            f"credentials/{self.client_id}/gmail_credentials.json"),
                "token_path": os.getenv(f"{prefix}GMAIL_TOKEN_PATH", 
                                      f"tokens/{self.client_id}/gmail_token.pickle")
            },
            "telegram": {
                "token": os.getenv(f"{prefix}TELEGRAM_TOKEN"),
                "chat_id": os.getenv(f"{prefix}TELEGRAM_CHAT_ID")
            },
            "pdf_tools": {
                "api_key": os.getenv(f"{prefix}PDF_API_KEY")
            },
            "elevenlabs": {
                "api_key": os.getenv(f"{prefix}ELEVENLABS_API_KEY")
            },
            "supabase": {
                "url": os.getenv(f"{prefix}SUPABASE_URL"),
                "key": os.getenv(f"{prefix}SUPABASE_KEY")
            },
            "instagram": {
                "access_token": os.getenv(f"{prefix}INSTAGRAM_ACCESS_TOKEN"),
                "app_id": os.getenv(f"{prefix}FACEBOOK_APP_ID"),
                "app_secret": os.getenv(f"{prefix}FACEBOOK_APP_SECRET"),
                "account_id": os.getenv(f"{prefix}INSTAGRAM_ACCOUNT_ID"),
                "page_id": os.getenv(f"{prefix}FACEBOOK_PAGE_ID")
            },
            "tiktok": {
                "client_key": os.getenv(f"{prefix}TIKTOK_CLIENT_KEY"),
                "client_secret": os.getenv(f"{prefix}TIKTOK_CLIENT_SECRET"),
                "access_token": os.getenv(f"{prefix}TIKTOK_ACCESS_TOKEN"),
                "refresh_token": os.getenv(f"{prefix}TIKTOK_REFRESH_TOKEN")
            },
            "dropbox": {
                "access_token": os.getenv(f"{prefix}DROPBOX_ACCESS_TOKEN"),
                "refresh_token": os.getenv(f"{prefix}DROPBOX_REFRESH_TOKEN"),
                "app_key": os.getenv(f"{prefix}DROPBOX_APP_KEY"),
                "app_secret": os.getenv(f"{prefix}DROPBOX_APP_SECRET")
            }
        }
        
        return config
    
    def get(self, service: str, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self.config.get(service, {}).get(key, default)
    
    def get_service_config(self, service: str) -> Dict[str, Any]:
        """Get all configuration for a service"""
        return self.config.get(service, {})
    
    def create_client_config_template(self, client_id: str) -> str:
        """Create a configuration template for a new client"""
        
        template = {
            "client_info": {
                "name": f"Client {client_id}",
                "description": "Configuration for MCP servers",
                "created": "2024-01-01"
            },
            "gmail": {
                "credentials_path": f"credentials/{client_id}/gmail_credentials.json",
                "token_path": f"tokens/{client_id}/gmail_token.pickle",
                "scopes": ["https://www.googleapis.com/auth/gmail.modify"]
            },
            "telegram": {
                "token": "your_telegram_bot_token",
                "chat_id": "your_default_chat_id",
                "parse_mode": "HTML"
            },
            "pdf_tools": {
                "api_key": "your_pdfshift_api_key",
                "default_format": "A4",
                "default_margin": 20
            },
            "elevenlabs": {
                "api_key": "your_elevenlabs_api_key",
                "default_voice": "rachel",
                "default_model": "eleven_monolingual_v1"
            },
            "supabase": {
                "url": "your_supabase_url",
                "key": "your_supabase_anon_key",
                "table_prefix": client_id
            },
            "instagram": {
                "access_token": "your_instagram_access_token",
                "app_id": "your_facebook_app_id",
                "app_secret": "your_facebook_app_secret",
                "account_id": "your_instagram_business_account_id",
                "page_id": "your_facebook_page_id"
            },
            "tiktok": {
                "client_key": "your_tiktok_client_key",
                "client_secret": "your_tiktok_client_secret",
                "access_token": "your_tiktok_access_token",
                "refresh_token": "your_tiktok_refresh_token"
            },
            "dropbox": {
                "access_token": "your_dropbox_access_token",
                "refresh_token": "your_dropbox_refresh_token",
                "app_key": "your_dropbox_app_key",
                "app_secret": "your_dropbox_app_secret"
            },
            "calendar": {
                "timezone": "UTC",
                "business_hours": {
                    "start": "09:00",
                    "end": "17:00"
                },
                "excluded_days": ["saturday", "sunday"]
            }
        }
        
        # Create config file
        config_file = self.config_dir / f"{client_id}.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(template, f, default_flow_style=False, indent=2)
        
        # Create directories
        Path(f"credentials/{client_id}").mkdir(parents=True, exist_ok=True)
        Path(f"tokens/{client_id}").mkdir(parents=True, exist_ok=True)
        
        return str(config_file)

# Global config manager - can be overridden
config = ConfigManager()

def set_client(client_id: str):
    """Set the global client configuration"""
    global config
    config = ConfigManager(client_id)
    return config 