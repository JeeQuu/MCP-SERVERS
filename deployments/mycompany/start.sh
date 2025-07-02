#!/bin/bash
# Start MCP servers for client: mycompany

export MCP_CLIENT_ID=mycompany

echo "🚀 Starting MCP servers for client: mycompany"

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
echo "$GMAIL_PID" > deployments/mycompany/gmail.pid
echo "$TELEGRAM_PID" > deployments/mycompany/telegram.pid
echo "$PDF_PID" > deployments/mycompany/pdf.pid
echo "$CALENDAR_PID" > deployments/mycompany/calendar.pid
echo "$INSTAGRAM_PID" > deployments/mycompany/instagram.pid
echo "$TIKTOK_PID" > deployments/mycompany/tiktok.pid

echo "💡 To stop servers, run: python deploy_client.py --stop mycompany"

wait
