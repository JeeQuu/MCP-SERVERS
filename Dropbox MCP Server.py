#!/usr/bin/env python3

"""
Dropbox MCP Server
Provides Dropbox integration capabilities for MCP clients.
Uses modern Streamable HTTP transport (built-in MCP SDK v1.10.1+)
"""

import os
import sys
from datetime import datetime
from mcp.server.fastmcp import FastMCP, Context
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create MCP server with modern Streamable HTTP support
mcp = FastMCP("Dropbox MCP Server")

def get_dropbox_client():
    """Get Dropbox client configuration"""
    access_token = os.getenv("DROPBOX_ACCESS_TOKEN")
    if not access_token:
        raise ValueError("DROPBOX_ACCESS_TOKEN environment variable not set")
    
    try:
        import dropbox
        return dropbox.Dropbox(access_token)
    except ImportError:
        raise ImportError("dropbox package not installed. Install with: pip install dropbox")

# Health check routes (CRITICAL for deployment)
@mcp.get("/")
async def health_check():
    """Health check endpoint for deployment services"""
    return {"status": "healthy", "service": "Dropbox MCP Server", "version": "1.0.0"}

@mcp.get("/health")
async def health_check_detailed():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "service": "Dropbox MCP Server",
        "version": "1.0.0",
        "transport": "streamable-http",
        "timestamp": datetime.now().isoformat()
    }

@mcp.tool()
async def upload_file(local_path: str, dropbox_path: str, ctx: Context) -> str:
    """Upload a file to Dropbox"""
    try:
        await ctx.info(f"Uploading {local_path} to {dropbox_path}")
        
        dbx = get_dropbox_client()
        
        with open(local_path, 'rb') as f:
            file_content = f.read()
            
        # Upload the file
        import dropbox
        dbx.files_upload(file_content, dropbox_path, mode=dropbox.files.WriteMode.overwrite)
        
        await ctx.info(f"Successfully uploaded {local_path} to {dropbox_path}")
        return f"File uploaded successfully: {dropbox_path}"
        
    except FileNotFoundError:
        return f"Local file not found: {local_path}"
    except Exception as e:
        await ctx.error(f"Upload failed: {str(e)}")
        return f"Upload failed: {str(e)}"

@mcp.tool()
async def download_file(dropbox_path: str, local_path: str, ctx: Context) -> str:
    """Download a file from Dropbox"""
    try:
        await ctx.info(f"Downloading {dropbox_path} to {local_path}")
        
        dbx = get_dropbox_client()
        
        # Download the file
        metadata, response = dbx.files_download(dropbox_path)
        
        with open(local_path, 'wb') as f:
            f.write(response.content)
            
        await ctx.info(f"Successfully downloaded {dropbox_path} to {local_path}")
        return f"File downloaded successfully: {local_path}"
        
    except Exception as e:
        await ctx.error(f"Download failed: {str(e)}")
        return f"Download failed: {str(e)}"

@mcp.tool()
async def list_folder(folder_path: str, ctx: Context) -> str:
    """List contents of a Dropbox folder"""
    try:
        await ctx.info(f"Listing folder: {folder_path}")
        
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
            
        return output
        
    except Exception as e:
        await ctx.error(f"List folder failed: {str(e)}")
        return f"List folder failed: {str(e)}"

@mcp.tool()
async def create_folder(folder_path: str, ctx: Context) -> str:
    """Create a new folder in Dropbox"""
    try:
        await ctx.info(f"Creating folder: {folder_path}")
        
        dbx = get_dropbox_client()
        
        if not folder_path.startswith("/"):
            folder_path = "/" + folder_path
            
        dbx.files_create_folder_v2(folder_path)
        
        await ctx.info(f"Successfully created folder: {folder_path}")
        return f"Folder created successfully: {folder_path}"
        
    except Exception as e:
        await ctx.error(f"Create folder failed: {str(e)}")
        return f"Create folder failed: {str(e)}"

@mcp.tool()
async def delete_file(dropbox_path: str, ctx: Context) -> str:
    """Delete a file or folder from Dropbox"""
    try:
        await ctx.info(f"Deleting: {dropbox_path}")
        
        dbx = get_dropbox_client()
        
        if not dropbox_path.startswith("/"):
            dropbox_path = "/" + dropbox_path
            
        dbx.files_delete_v2(dropbox_path)
        
        await ctx.info(f"Successfully deleted: {dropbox_path}")
        return f"Deleted successfully: {dropbox_path}"
        
    except Exception as e:
        await ctx.error(f"Delete failed: {str(e)}")
        return f"Delete failed: {str(e)}"

@mcp.tool()
async def get_file_info(dropbox_path: str, ctx: Context) -> str:
    """Get information about a file or folder"""
    try:
        await ctx.info(f"Getting info for: {dropbox_path}")
        
        dbx = get_dropbox_client()
        
        if not dropbox_path.startswith("/"):
            dropbox_path = "/" + dropbox_path
            
        metadata = dbx.files_get_metadata(dropbox_path)
        
        import dropbox
        if isinstance(metadata, dropbox.files.FileMetadata):
            return f"""File Info:
Name: {metadata.name}
Path: {metadata.path_display}
Size: {metadata.size} bytes
Modified: {metadata.client_modified}
Content Hash: {metadata.content_hash}"""
        elif isinstance(metadata, dropbox.files.FolderMetadata):
            return f"""Folder Info:
Name: {metadata.name}
Path: {metadata.path_display}
Type: Folder"""
        else:
            return f"Unknown file type: {type(metadata)}"
            
    except Exception as e:
        await ctx.error(f"Get file info failed: {str(e)}")
        return f"Get file info failed: {str(e)}"

@mcp.tool()
async def create_shared_link(dropbox_path: str, ctx: Context) -> str:
    """Create a shared link for a file or folder"""
    try:
        await ctx.info(f"Creating shared link for: {dropbox_path}")
        
        dbx = get_dropbox_client()
        
        if not dropbox_path.startswith("/"):
            dropbox_path = "/" + dropbox_path
            
        # Try to get existing shared link first
        try:
            links = dbx.sharing_list_shared_links(path=dropbox_path, direct_only=True)
            if links.links:
                link_url = links.links[0].url
                await ctx.info(f"Using existing shared link: {link_url}")
                return f"Shared link: {link_url}"
        except:
            pass
            
        # Create new shared link
        shared_link = dbx.sharing_create_shared_link_with_settings(dropbox_path)
        link_url = shared_link.url
        
        await ctx.info(f"Created shared link: {link_url}")
        return f"Shared link created: {link_url}"
        
    except Exception as e:
        await ctx.error(f"Create shared link failed: {str(e)}")
        return f"Create shared link failed: {str(e)}"

@mcp.tool()
async def search_files(query: str, ctx: Context) -> str:
    """Search for files in Dropbox"""
    try:
        await ctx.info(f"Searching for: {query}")
        
        dbx = get_dropbox_client()
        
        result = dbx.files_search_v2(query)
        
        if not result.matches:
            return f"No files found matching: {query}"
            
        matches = []
        import dropbox
        for match in result.matches[:10]:  # Limit to first 10 results
            metadata = match.metadata.metadata
            if isinstance(metadata, dropbox.files.FileMetadata):
                matches.append(f"📄 {metadata.path_display} ({metadata.size} bytes)")
            elif isinstance(metadata, dropbox.files.FolderMetadata):
                matches.append(f"📁 {metadata.path_display}/")
                
        return f"Search results for '{query}':\n" + "\n".join(matches)
        
    except Exception as e:
        await ctx.error(f"Search failed: {str(e)}")
        return f"Search failed: {str(e)}"

@mcp.tool()
async def get_account_info(ctx: Context) -> str:
    """Get Dropbox account information"""
    try:
        await ctx.info("Getting account information")
        
        dbx = get_dropbox_client()
        
        account = dbx.users_get_current_account()
        space_usage = dbx.users_get_space_usage()
        
        used = space_usage.used
        allocated = space_usage.allocation.get_individual().allocated
        
        return f"""Dropbox Account Info:
Name: {account.name.display_name}
Email: {account.email}
Account Type: {account.account_type._tag_}
Storage Used: {used / (1024**3):.2f} GB
Storage Total: {allocated / (1024**3):.2f} GB
Storage Available: {(allocated - used) / (1024**3):.2f} GB"""
        
    except Exception as e:
        await ctx.error(f"Get account info failed: {str(e)}")
        return f"Get account info failed: {str(e)}"

def main():
    """Main entry point"""
    port = int(os.getenv("PORT", "8001"))
    
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        # Run with stdio transport for local development
        print("🔧 Running Dropbox MCP Server with stdio transport", file=sys.stderr)
        mcp.run(transport="stdio")
    else:
        # Run with modern Streamable HTTP transport for production
        print(f"🚀 Starting Dropbox MCP Server with Streamable HTTP on port {port}", file=sys.stderr)
        print(f"📡 Streamable HTTP endpoint: http://localhost:{port}/mcp", file=sys.stderr)
        print(f"❤️  Health check endpoint: http://localhost:{port}/", file=sys.stderr)
        
        # Configure for production deployment
        mcp.settings.host = "0.0.0.0"  # Accept connections from any host
        mcp.settings.port = port
        mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main() 