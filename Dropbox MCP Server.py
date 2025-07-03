#!/usr/bin/env python3

"""
Dropbox MCP Server
Provides Dropbox integration capabilities for MCP clients.
Uses basic MCP server with custom HTTP wrapper for Render deployment
"""

import os
import sys
import asyncio
from datetime import datetime
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create MCP server with basic server for full control
server = Server("Dropbox MCP Server")

def get_dropbox_client():
    """Get Dropbox client configuration"""
    access_token = os.getenv("DROPBOX_ACCESS_TOKEN")
    if not access_token:
        raise ValueError("DROPBOX_ACCESS_TOKEN environment variable not set. Please set this in your Render environment variables.")
    
    try:
        import dropbox
        return dropbox.Dropbox(access_token)
    except ImportError:
        raise ImportError("dropbox package not installed. Install with: pip install dropbox")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="upload_file",
            description="Upload a file to Dropbox",
            inputSchema={
                "type": "object",
                "properties": {
                    "local_path": {"type": "string", "description": "Local file path to upload"},
                    "dropbox_path": {"type": "string", "description": "Destination path in Dropbox"}
                },
                "required": ["local_path", "dropbox_path"]
            }
        ),
        Tool(
            name="download_file", 
            description="Download a file from Dropbox",
            inputSchema={
                "type": "object",
                "properties": {
                    "dropbox_path": {"type": "string", "description": "Path to file in Dropbox"},
                    "local_path": {"type": "string", "description": "Local destination path"}
                },
                "required": ["dropbox_path", "local_path"]
            }
        ),
        Tool(
            name="list_folder",
            description="List contents of a Dropbox folder",
            inputSchema={
                "type": "object",
                "properties": {
                    "folder_path": {"type": "string", "description": "Dropbox folder path to list"}
                },
                "required": ["folder_path"]
            }
        ),
        Tool(
            name="create_folder",
            description="Create a new folder in Dropbox",
            inputSchema={
                "type": "object",
                "properties": {
                    "folder_path": {"type": "string", "description": "Path for the new folder"}
                },
                "required": ["folder_path"]
            }
        ),
        Tool(
            name="delete_file",
            description="Delete a file or folder from Dropbox",
            inputSchema={
                "type": "object",
                "properties": {
                    "dropbox_path": {"type": "string", "description": "Path to file/folder to delete"}
                },
                "required": ["dropbox_path"]
            }
        ),
        Tool(
            name="get_file_info",
            description="Get information about a file or folder",
            inputSchema={
                "type": "object",
                "properties": {
                    "dropbox_path": {"type": "string", "description": "Path to file/folder"}
                },
                "required": ["dropbox_path"]
            }
        ),
        Tool(
            name="create_shared_link",
            description="Create a shared link for a file or folder",
            inputSchema={
                "type": "object",
                "properties": {
                    "dropbox_path": {"type": "string", "description": "Path to file/folder to share"}
                },
                "required": ["dropbox_path"]
            }
        ),
        Tool(
            name="search_files",
            description="Search for files in Dropbox",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_account_info",
            description="Get Dropbox account information",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls"""
    try:
        if name == "upload_file":
            local_path = arguments.get("local_path", "")
            dropbox_path = arguments.get("dropbox_path", "")
            
            try:
                dbx = get_dropbox_client()
                
                with open(local_path, 'rb') as f:
                    file_content = f.read()
                    
                # Import dropbox for WriteMode
                import dropbox
                dbx.files_upload(file_content, dropbox_path, mode=dropbox.files.WriteMode.overwrite)
                
                return [TextContent(type="text", text=f"File uploaded successfully: {dropbox_path}")]
                
            except FileNotFoundError:
                return [TextContent(type="text", text=f"Local file not found: {local_path}")]
            except Exception as e:
                return [TextContent(type="text", text=f"Upload failed: {str(e)}")]
        
        elif name == "download_file":
            dropbox_path = arguments.get("dropbox_path", "")
            local_path = arguments.get("local_path", "")
            
            try:
                dbx = get_dropbox_client()
                
                # Download the file
                metadata, response = dbx.files_download(dropbox_path)
                
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                    
                return [TextContent(type="text", text=f"File downloaded successfully: {local_path}")]
                
            except Exception as e:
                return [TextContent(type="text", text=f"Download failed: {str(e)}")]
        
        elif name == "list_folder":
            folder_path = arguments.get("folder_path", "")
            
            try:
                dbx = get_dropbox_client()
                
                # Normalize folder path
                if folder_path == "/" or folder_path == "":
                    folder_path = ""
                elif not folder_path.startswith("/"):
                    folder_path = "/" + folder_path
                    
                result = dbx.files_list_folder(folder_path)
                
                files = []
                folders = []
                
                import dropbox
                for entry in result.entries:
                    if isinstance(entry, dropbox.files.FileMetadata):
                        files.append(f"📄 {entry.name} ({entry.size} bytes)")
                    elif isinstance(entry, dropbox.files.FolderMetadata):
                        folders.append(f"📁 {entry.name}/")
                        
                output = f"Contents of {folder_path or '/'}:\n"
                if folders:
                    output += "\nFolders:\n" + "\n".join(folders)
                if files:
                    output += "\nFiles:\n" + "\n".join(files)
                    
                return [TextContent(type="text", text=output)]
                
            except Exception as e:
                return [TextContent(type="text", text=f"List folder failed: {str(e)}")]
        
        elif name == "create_folder":
            folder_path = arguments.get("folder_path", "")
            
            try:
                dbx = get_dropbox_client()
                
                if not folder_path.startswith("/"):
                    folder_path = "/" + folder_path
                    
                dbx.files_create_folder_v2(folder_path)
                
                return [TextContent(type="text", text=f"Folder created successfully: {folder_path}")]
                
            except Exception as e:
                return [TextContent(type="text", text=f"Create folder failed: {str(e)}")]
        
        elif name == "delete_file":
            dropbox_path = arguments.get("dropbox_path", "")
            
            try:
                dbx = get_dropbox_client()
                
                if not dropbox_path.startswith("/"):
                    dropbox_path = "/" + dropbox_path
                    
                dbx.files_delete_v2(dropbox_path)
                
                return [TextContent(type="text", text=f"Deleted successfully: {dropbox_path}")]
                
            except Exception as e:
                return [TextContent(type="text", text=f"Delete failed: {str(e)}")]
        
        elif name == "get_file_info":
            dropbox_path = arguments.get("dropbox_path", "")
            
            try:
                dbx = get_dropbox_client()
                
                if not dropbox_path.startswith("/"):
                    dropbox_path = "/" + dropbox_path
                    
                metadata = dbx.files_get_metadata(dropbox_path)
                
                import dropbox
                if isinstance(metadata, dropbox.files.FileMetadata):
                    result = f"""File Info:
Name: {metadata.name}
Path: {metadata.path_display}
Size: {metadata.size} bytes
Modified: {metadata.client_modified}
Content Hash: {metadata.content_hash}"""
                elif isinstance(metadata, dropbox.files.FolderMetadata):
                    result = f"""Folder Info:
Name: {metadata.name}
Path: {metadata.path_display}
Type: Folder"""
                else:
                    result = f"Unknown file type: {type(metadata)}"
                    
                return [TextContent(type="text", text=result)]
                
            except Exception as e:
                return [TextContent(type="text", text=f"Get file info failed: {str(e)}")]
        
        elif name == "create_shared_link":
            dropbox_path = arguments.get("dropbox_path", "")
            
            try:
                dbx = get_dropbox_client()
                
                if not dropbox_path.startswith("/"):
                    dropbox_path = "/" + dropbox_path
                    
                # Try to get existing shared link first
                try:
                    links = dbx.sharing_list_shared_links(path=dropbox_path, direct_only=True)
                    if links.links:
                        link_url = links.links[0].url
                        return [TextContent(type="text", text=f"Shared link: {link_url}")]
                except:
                    pass
                    
                # Create new shared link
                shared_link = dbx.sharing_create_shared_link_with_settings(dropbox_path)
                link_url = shared_link.url
                
                return [TextContent(type="text", text=f"Shared link created: {link_url}")]
                
            except Exception as e:
                return [TextContent(type="text", text=f"Create shared link failed: {str(e)}")]
        
        elif name == "search_files":
            query = arguments.get("query", "")
            
            try:
                dbx = get_dropbox_client()
                
                result = dbx.files_search_v2(query)
                
                if not result.matches:
                    return [TextContent(type="text", text=f"No files found matching: {query}")]
                    
                matches = []
                import dropbox
                for match in result.matches[:10]:  # Limit to first 10 results
                    metadata = match.metadata.metadata
                    if isinstance(metadata, dropbox.files.FileMetadata):
                        matches.append(f"📄 {metadata.path_display} ({metadata.size} bytes)")
                    elif isinstance(metadata, dropbox.files.FolderMetadata):
                        matches.append(f"📁 {metadata.path_display}/")
                        
                return [TextContent(type="text", text=f"Search results for '{query}':\n" + "\n".join(matches))]
                
            except Exception as e:
                return [TextContent(type="text", text=f"Search failed: {str(e)}")]
        
        elif name == "get_account_info":
            try:
                dbx = get_dropbox_client()
                
                account = dbx.users_get_current_account()
                space_usage = dbx.users_get_space_usage()
                
                used = space_usage.used
                allocated = space_usage.allocation.get_individual().allocated
                
                result = f"""Dropbox Account Info:
Name: {account.name.display_name}
Email: {account.email}
Account Type: {account.account_type._tag_}
Storage Used: {used / (1024**3):.2f} GB
Storage Total: {allocated / (1024**3):.2f} GB
Storage Available: {(allocated - used) / (1024**3):.2f} GB"""
                
                return [TextContent(type="text", text=result)]
                
            except Exception as e:
                return [TextContent(type="text", text=f"Get account info failed: {str(e)}")]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
            
    except Exception as e:
        return [TextContent(type="text", text=f"Tool execution failed: {str(e)}")]

async def main():
    """Main entry point"""
    port = int(os.getenv("PORT", "8000"))
    
    # For Render deployment - just run a simple health check server
    print(f"🚀 Starting Simple Dropbox MCP Server on port {port}", file=sys.stderr)
    print(f"🌍 Environment: {os.getenv('RENDER', 'local')}", file=sys.stderr)
    
    # Import transport components
    from starlette.applications import Starlette
    from starlette.routing import Route
    from starlette.responses import JSONResponse
    import uvicorn
    
    async def health_check(request):
        return JSONResponse({
            "status": "healthy", 
            "service": "Dropbox MCP Server",
            "version": "1.0.0",
            "transport": "http",
            "timestamp": datetime.now().isoformat(),
            "dropbox_configured": bool(os.getenv("DROPBOX_ACCESS_TOKEN")),
            "port": port,
            "message": "Simple health check working"
        })
    
    # Create Starlette app with health check
    app = Starlette(routes=[
        Route("/", health_check),
        Route("/health", health_check),
    ])
    
    print(f"✅ Health check routes configured", file=sys.stderr)
    print(f"🚀 Starting server on http://0.0.0.0:{port}", file=sys.stderr)
    
    # Run with uvicorn
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
    server_instance = uvicorn.Server(config)
    await server_instance.serve()

if __name__ == "__main__":
    asyncio.run(main()) 