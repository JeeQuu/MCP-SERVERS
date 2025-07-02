FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py ./
COPY configs/ ./configs/
COPY credentials/ ./credentials/
COPY tokens/ ./tokens/

# Create volume mount points
VOLUME ["/app/configs", "/app/credentials", "/app/tokens"]

# Environment variables
ENV MCP_CLIENT_ID=default
ENV PYTHONPATH=/app

# Default command (can be overridden)
CMD ["python", "Gmail MPC Server.py"] 