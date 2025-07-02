#!/usr/bin/env python3

"""
PDF Tools MCP Server
Provides PDF processing and manipulation capabilities for MCP clients.
Uses modern Streamable HTTP transport (built-in MCP SDK v1.10.1+)
"""

import os
import sys
import base64
from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import FastMCP, Context
from dotenv import load_dotenv
import tempfile
import requests

# Load environment variables
load_dotenv()

# Create MCP server with modern Streamable HTTP support
mcp = FastMCP("PDF Tools MCP Server")

def get_pdf_libraries():
    """Check and import required PDF libraries"""
    try:
        import PyPDF2
        import reportlab
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        return PyPDF2, reportlab, canvas, letter
    except ImportError as e:
        raise ImportError(f"Required PDF libraries not installed. Install with: pip install PyPDF2 reportlab. Error: {e}")

@mcp.tool()
async def extract_text_from_pdf(pdf_url: str, ctx: Context) -> str:
    """Extract text content from a PDF file"""
    try:
        await ctx.info(f"Extracting text from PDF: {pdf_url}")
        
        PyPDF2, _, _, _ = get_pdf_libraries()
        
        # Download PDF
        response = requests.get(pdf_url)
        if response.status_code != 200:
            return f"Failed to download PDF from {pdf_url}"
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(response.content)
            temp_path = temp_file.name
        
        try:
            # Extract text using PyPDF2
            with open(temp_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                total_pages = len(pdf_reader.pages)
                extracted_text = ""
                
                for page_num in range(total_pages):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    extracted_text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                
                await ctx.info(f"Successfully extracted text from {total_pages} pages")
                
                result = f"PDF Text Extraction Results:\n"
                result += f"Source: {pdf_url}\n"
                result += f"Total Pages: {total_pages}\n"
                result += f"Content Length: {len(extracted_text)} characters\n\n"
                result += extracted_text[:2000]  # Limit output
                
                if len(extracted_text) > 2000:
                    result += f"\n\n... (truncated, total length: {len(extracted_text)} characters)"
                
                return result
                
        finally:
            # Clean up temporary file
            os.unlink(temp_path)
        
    except Exception as e:
        await ctx.error(f"Failed to extract text from PDF: {str(e)}")
        return f"Failed to extract text from PDF: {str(e)}"

@mcp.tool()
async def get_pdf_info(pdf_url: str, ctx: Context) -> str:
    """Get metadata and information about a PDF file"""
    try:
        await ctx.info(f"Getting PDF info for: {pdf_url}")
        
        PyPDF2, _, _, _ = get_pdf_libraries()
        
        # Download PDF
        response = requests.get(pdf_url)
        if response.status_code != 200:
            return f"Failed to download PDF from {pdf_url}"
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(response.content)
            temp_path = temp_file.name
        
        try:
            # Get PDF info using PyPDF2
            with open(temp_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Basic info
                total_pages = len(pdf_reader.pages)
                
                # Metadata
                metadata = pdf_reader.metadata if pdf_reader.metadata else {}
                
                # First page dimensions
                first_page = pdf_reader.pages[0]
                page_box = first_page.mediabox
                
                result = f"""PDF Information:
📄 Source: {pdf_url}
📊 Total Pages: {total_pages}
📏 Page Size: {float(page_box.width)} x {float(page_box.height)} pts

📋 Metadata:
• Title: {metadata.get('/Title', 'Not specified')}
• Author: {metadata.get('/Author', 'Not specified')}
• Subject: {metadata.get('/Subject', 'Not specified')}
• Creator: {metadata.get('/Creator', 'Not specified')}
• Producer: {metadata.get('/Producer', 'Not specified')}
• Creation Date: {metadata.get('/CreationDate', 'Not specified')}
• Modification Date: {metadata.get('/ModDate', 'Not specified')}

📁 File Size: {len(response.content)} bytes ({len(response.content) / 1024:.1f} KB)"""
                
                await ctx.info(f"Retrieved info for PDF with {total_pages} pages")
                return result
                
        finally:
            # Clean up temporary file
            os.unlink(temp_path)
        
    except Exception as e:
        await ctx.error(f"Failed to get PDF info: {str(e)}")
        return f"Failed to get PDF info: {str(e)}"

@mcp.tool()
async def split_pdf_pages(pdf_url: str, start_page: int, end_page: int, ctx: Context) -> str:
    """Split a PDF and extract specific pages"""
    try:
        await ctx.info(f"Splitting PDF pages {start_page}-{end_page} from: {pdf_url}")
        
        PyPDF2, _, _, _ = get_pdf_libraries()
        
        # Download PDF
        response = requests.get(pdf_url)
        if response.status_code != 200:
            return f"Failed to download PDF from {pdf_url}"
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(response.content)
            temp_path = temp_file.name
        
        try:
            # Split PDF using PyPDF2
            with open(temp_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pdf_writer = PyPDF2.PdfWriter()
                
                total_pages = len(pdf_reader.pages)
                
                # Validate page range
                if start_page < 1 or end_page > total_pages or start_page > end_page:
                    return f"Invalid page range: {start_page}-{end_page}. PDF has {total_pages} pages."
                
                # Add specified pages to writer
                for page_num in range(start_page - 1, end_page):  # Convert to 0-based indexing
                    pdf_writer.add_page(pdf_reader.pages[page_num])
                
                # Save split PDF to temporary file
                with tempfile.NamedTemporaryFile(suffix='_split.pdf', delete=False) as output_file:
                    pdf_writer.write(output_file)
                    output_path = output_file.name
                
                # Read the split PDF and convert to base64
                with open(output_path, 'rb') as split_file:
                    split_pdf_data = split_file.read()
                    base64_data = base64.b64encode(split_pdf_data).decode('utf-8')
                
                # Clean up output file
                os.unlink(output_path)
                
                pages_extracted = end_page - start_page + 1
                
                await ctx.info(f"Successfully split PDF: extracted {pages_extracted} pages")
                
                result = f"""PDF Split Results:
📄 Source: {pdf_url}
📊 Original Pages: {total_pages}
✂️  Extracted Pages: {start_page}-{end_page} ({pages_extracted} pages)
📁 Output Size: {len(split_pdf_data)} bytes

📋 Base64 Data (first 100 chars):
{base64_data[:100]}...

💡 Use this base64 data to save the split PDF file."""
                
                return result
                
        finally:
            # Clean up input file
            os.unlink(temp_path)
        
    except Exception as e:
        await ctx.error(f"Failed to split PDF: {str(e)}")
        return f"Failed to split PDF: {str(e)}"

@mcp.tool()
async def create_pdf_from_text(text: str, title: str, ctx: Context) -> str:
    """Create a PDF document from text content"""
    try:
        await ctx.info(f"Creating PDF from text: {title}")
        
        _, _, canvas, letter = get_pdf_libraries()
        
        # Create PDF in temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # Create PDF using ReportLab
            c = canvas.Canvas(temp_path, pagesize=letter)
            width, height = letter
            
            # Add title
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, title)
            
            # Add text content
            c.setFont("Helvetica", 12)
            
            # Split text into lines that fit the page
            lines = text.split('\n')
            y_position = height - 100
            line_height = 14
            
            for line in lines:
                # Handle long lines by wrapping
                if len(line) > 80:  # Approximate character limit per line
                    words = line.split(' ')
                    current_line = ""
                    
                    for word in words:
                        if len(current_line + word) < 80:
                            current_line += word + " "
                        else:
                            if current_line:
                                c.drawString(50, y_position, current_line.strip())
                                y_position -= line_height
                                if y_position < 50:  # Start new page
                                    c.showPage()
                                    c.setFont("Helvetica", 12)
                                    y_position = height - 50
                            current_line = word + " "
                    
                    if current_line:
                        c.drawString(50, y_position, current_line.strip())
                        y_position -= line_height
                else:
                    c.drawString(50, y_position, line)
                    y_position -= line_height
                
                # Check if we need a new page
                if y_position < 50:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y_position = height - 50
            
            c.save()
            
            # Read the created PDF and convert to base64
            with open(temp_path, 'rb') as pdf_file:
                pdf_data = pdf_file.read()
                base64_data = base64.b64encode(pdf_data).decode('utf-8')
            
            await ctx.info(f"Successfully created PDF: {len(pdf_data)} bytes")
            
            result = f"""PDF Creation Results:
📄 Title: {title}
📊 Content Length: {len(text)} characters
📁 PDF Size: {len(pdf_data)} bytes
📑 Pages: Estimated {(len(text) // 2000) + 1}

📋 Base64 Data (first 100 chars):
{base64_data[:100]}...

💡 Use this base64 data to save the PDF file."""
            
            return result
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        
    except Exception as e:
        await ctx.error(f"Failed to create PDF: {str(e)}")
        return f"Failed to create PDF: {str(e)}"

@mcp.tool()
async def merge_pdfs(pdf_urls: List[str], ctx: Context) -> str:
    """Merge multiple PDF files into one"""
    try:
        await ctx.info(f"Merging {len(pdf_urls)} PDF files")
        
        PyPDF2, _, _, _ = get_pdf_libraries()
        
        pdf_writer = PyPDF2.PdfWriter()
        temp_files = []
        
        try:
            # Download and process each PDF
            for i, pdf_url in enumerate(pdf_urls):
                await ctx.info(f"Processing PDF {i+1}/{len(pdf_urls)}: {pdf_url}")
                
                # Download PDF
                response = requests.get(pdf_url)
                if response.status_code != 200:
                    return f"Failed to download PDF from {pdf_url}"
                
                # Save to temporary file
                with tempfile.NamedTemporaryFile(suffix=f'_{i}.pdf', delete=False) as temp_file:
                    temp_file.write(response.content)
                    temp_path = temp_file.name
                    temp_files.append(temp_path)
                
                # Add all pages to the writer
                with open(temp_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        pdf_writer.add_page(page)
            
            # Save merged PDF
            with tempfile.NamedTemporaryFile(suffix='_merged.pdf', delete=False) as output_file:
                pdf_writer.write(output_file)
                output_path = output_file.name
            
            # Read the merged PDF and convert to base64
            with open(output_path, 'rb') as merged_file:
                merged_pdf_data = merged_file.read()
                base64_data = base64.b64encode(merged_pdf_data).decode('utf-8')
            
            # Clean up output file
            os.unlink(output_path)
            
            total_pages = len(pdf_writer.pages)
            
            await ctx.info(f"Successfully merged {len(pdf_urls)} PDFs into {total_pages} pages")
            
            result = f"""PDF Merge Results:
📄 Source PDFs: {len(pdf_urls)}
📊 Total Pages: {total_pages}
📁 Output Size: {len(merged_pdf_data)} bytes

📋 Source URLs:
"""
            for i, url in enumerate(pdf_urls, 1):
                result += f"{i}. {url}\n"
            
            result += f"""
📋 Base64 Data (first 100 chars):
{base64_data[:100]}...

💡 Use this base64 data to save the merged PDF file."""
            
            return result
            
        finally:
            # Clean up all temporary files
            for temp_path in temp_files:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
        
    except Exception as e:
        await ctx.error(f"Failed to merge PDFs: {str(e)}")
        return f"Failed to merge PDFs: {str(e)}"

@mcp.tool()
async def search_pdf_text(pdf_url: str, search_term: str, ctx: Context) -> str:
    """Search for specific text within a PDF"""
    try:
        await ctx.info(f"Searching for '{search_term}' in PDF: {pdf_url}")
        
        PyPDF2, _, _, _ = get_pdf_libraries()
        
        # Download PDF
        response = requests.get(pdf_url)
        if response.status_code != 200:
            return f"Failed to download PDF from {pdf_url}"
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(response.content)
            temp_path = temp_file.name
        
        try:
            # Search through PDF
            with open(temp_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                total_pages = len(pdf_reader.pages)
                matches = []
                
                for page_num in range(total_pages):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    
                    if search_term.lower() in page_text.lower():
                        # Find context around the match
                        lines = page_text.split('\n')
                        for line_num, line in enumerate(lines):
                            if search_term.lower() in line.lower():
                                # Get context (previous and next lines)
                                start_line = max(0, line_num - 2)
                                end_line = min(len(lines), line_num + 3)
                                context_lines = lines[start_line:end_line]
                                context = '\n'.join(context_lines)
                                
                                matches.append({
                                    'page': page_num + 1,
                                    'line': line_num + 1,
                                    'context': context[:200] + '...' if len(context) > 200 else context
                                })
                
                await ctx.info(f"Found {len(matches)} matches across {total_pages} pages")
                
                result = f"""PDF Search Results:
📄 Source: {pdf_url}
🔍 Search Term: "{search_term}"
📊 Total Pages: {total_pages}
🎯 Matches Found: {len(matches)}

"""
                
                if matches:
                    result += "📋 Match Details:\n"
                    for i, match in enumerate(matches[:10], 1):  # Limit to first 10 matches
                        result += f"\nMatch {i}:\n"
                        result += f"  Page: {match['page']}, Line: {match['line']}\n"
                        result += f"  Context: {match['context']}\n"
                    
                    if len(matches) > 10:
                        result += f"\n... and {len(matches) - 10} more matches"
                else:
                    result += "❌ No matches found"
                
                return result
                
        finally:
            # Clean up temporary file
            os.unlink(temp_path)
        
    except Exception as e:
        await ctx.error(f"Failed to search PDF: {str(e)}")
        return f"Failed to search PDF: {str(e)}"

@mcp.resource("pdf://tools")
def get_pdf_tools() -> str:
    """Get PDF tools resource"""
    try:
        get_pdf_libraries()  # Test if libraries are available
        return "PDF Tools: PyPDF2 and ReportLab libraries available"
    except ImportError as e:
        return f"PDF Tools: Missing dependencies - {str(e)}"

@mcp.resource("pdf://config")
def get_pdf_config() -> str:
    """Get PDF Tools server configuration"""
    return """PDF Tools MCP Server Configuration:
- Modern Streamable HTTP Transport ✅
- Text Extraction ✅
- PDF Information ✅
- Page Splitting ✅
- PDF Creation ✅
- PDF Merging ✅
- Text Search ✅
- Async Context Support ✅"""

def main():
    """Main entry point"""
    port = int(os.getenv("PORT", "8006"))
    
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        # Run with stdio transport for local development
        print("🔧 Running PDF Tools MCP Server with stdio transport", file=sys.stderr)
        mcp.run(transport="stdio")
    else:
        # Run with modern Streamable HTTP transport for production
        print(f"🚀 Starting PDF Tools MCP Server with Streamable HTTP on port {port}", file=sys.stderr)
        print(f"📡 Streamable HTTP endpoint: http://localhost:{port}/mcp", file=sys.stderr)
        print(f"❤️  Health check endpoint: http://localhost:{port}/", file=sys.stderr)
        
        # Configure for production deployment
        mcp.settings.host = "0.0.0.0"  # Accept connections from any host
        mcp.settings.port = port
        mcp.run(transport="streamable-http")

if __name__ == "__main__":
    main()