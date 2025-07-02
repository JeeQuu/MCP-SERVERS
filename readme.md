# MCP Server Collection for n8n Workflows

A powerful collection of MCP (Model Control Protocol) servers designed for seamless integration with n8n to create sophisticated automation workflows.

## 🚀 Available Servers

### 📅 Calendar MCP Server
Smart scheduling and calendar management with natural language processing.

**Features:**
- Natural language date parsing ("next Tuesday at 3pm")
- Event creation and conflict detection
- Available time slot finding
- Recurring events support
- Smart scheduling suggestions

**Tools:**
- `parse_natural_date` - Parse human-friendly dates
- `create_event` - Create calendar events
- `find_available_slots` - Find free time slots
- `list_events` - List upcoming events
- `check_conflicts` - Check for scheduling conflicts
- `create_recurring_event` - Create recurring events

### 📧 Gmail MCP Server
Professional email operations with full Gmail API integration.

**Features:**
- Advanced email search with Gmail query syntax
- Send emails with HTML formatting
- Draft management
- Label operations
- Email threading support
- Attachment handling

**Tools:**
- `search_emails` - Search emails with advanced queries
- `get_email` - Get full email details
- `send_email` - Send formatted emails
- `create_draft` - Create email drafts
- `modify_labels` - Add/remove labels
- `archive_email` - Archive emails
- `mark_as_read` - Mark as read/unread

### 💬 Telegram MCP Server
Real-time messaging and notification system.

**Features:**
- Send text messages with HTML formatting
- Interactive inline keyboards
- Document sharing
- Message editing
- Status updates with visual indicators
- Formatted list displays

**Tools:**
- `send_message` - Send text messages
- `send_message_with_buttons` - Send interactive messages
- `send_document` - Share documents
- `edit_message` - Edit existing messages
- `send_formatted_list` - Send structured lists
- `send_status_update` - Send status notifications

### 📄 PDF Tools MCP Server
Comprehensive PDF processing and generation.

**Features:**
- HTML to PDF conversion
- Text extraction from PDFs
- PDF merging and splitting
- Invoice generation
- Watermark addition
- Format conversion

**Tools:**
- `html_to_pdf` - Convert HTML to PDF
- `extract_text` - Extract text from PDFs
- `merge_pdfs` - Merge multiple PDFs
- `split_pdf` - Split PDFs at specific pages
- `create_invoice_pdf` - Generate professional invoices
- `add_watermark` - Add watermarks to PDFs

### 🗄️ Supabase MCP Server
Database operations and real-time data management.

### 🎤 ElevenLabs MCP Server
AI-powered voice synthesis and audio generation.

### 📸 Instagram MCP Server
Complete Instagram automation and content management.

**Features:**
- Post photos, videos, and carousels
- Get account insights and analytics
- Retrieve recent media and posts
- Account information management
- Stories creation
- Hashtag research
- Performance tracking

**Tools:**
- `instagram_post_photo` - Post photos to Instagram
- `instagram_get_insights` - Get account analytics
- `instagram_get_recent_media` - Retrieve recent posts
- `instagram_get_account_info` - Get account information

### 🎵 TikTok MCP Server
TikTok analytics, trending research, and content optimization.

**Features:**
- User account analytics and stats
- Trending hashtag analysis
- Content performance insights
- Hashtag research and optimization
- Posting time recommendations
- Engagement rate calculations
- Content strategy insights

**Tools:**
- `tiktok_get_user_info` - Get account information and stats
- `tiktok_get_trending_hashtags` - Discover trending hashtags
- `tiktok_search_hashtags` - Analyze hashtag performance
- `tiktok_get_content_insights` - Get comprehensive analytics

### ☁️ Dropbox MCP Server
Cloud storage automation and file management.

**Features:**
- File upload and download with base64 support
- Folder listing and navigation
- File search across your Dropbox
- Shared link creation with expiration and passwords
- Account information and storage usage
- Batch operations and file management
- Automatic path handling and error recovery

**Tools:**
- `dropbox_upload` - Upload files to Dropbox
- `dropbox_download` - Download files from Dropbox
- `dropbox_list_folder` - List folder contents
- `dropbox_create_shared_link` - Create shareable links
- `dropbox_search` - Search for files
- `dropbox_account_info` - Get account information
- `dropbox_space_usage` - Check storage usage

## ➕ **Adding New Services (Super Easy!)**

Your architecture is designed for continuous expansion! Here's how simple it is:

### **Step 1: Create New Server** (5 minutes)
```python
# Follow the same pattern as existing servers
class NewServiceMCP:
    def __init__(self, client_id: Optional[str] = None):
        if client_id:
            set_client(client_id)
        
        self.api_key = config.get("newservice", "api_key")
        # ... rest of initialization
```

### **Step 2: Update Configuration** (2 minutes)
1. **Add to `config_manager.py`**: Include service credentials
2. **Update `render.yaml`**: Add new service deployment
3. **Update `render-env-template.txt`**: Add environment variables

### **Step 3: Deploy** (1 minute)
```bash
git add . && git commit -m "Added NewService" && git push
# Render automatically deploys your new service!
```

### **🔥 Just Added: Dropbox Server!**
We just demonstrated this by adding **Dropbox** in under 5 minutes:
- ✅ **Full Dropbox API integration**
- ✅ **File upload/download/search**
- ✅ **Shared link creation**
- ✅ **Multi-client support**
- ✅ **Render deployment ready**

**Total time**: 5 minutes from idea to production-ready service!

### **Popular Services to Add Next:**
- **Google Drive** (similar to Dropbox)
- **Slack** (team messaging)
- **Discord** (community management)
- **Airtable** (database management)
- **Notion** (document automation)
- **Stripe** (payment processing)
- **Shopify** (e-commerce)
- **OpenAI** (AI completions)

---

## 🛠️ Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Multi-Client Configuration System

This system supports multiple clients with separate configurations and credentials. Each client gets their own isolated environment.

#### For Your Own Use (Single Client)
```bash
# Set up your personal configuration
python deploy_client.py --setup mycompany --name "My Company"

# Edit the generated config file
# configs/mycompany.yaml

# Add your credentials and API keys
# Then run your servers
python deploy_client.py --run mycompany
```

#### For Multiple Clients
```bash
# Set up different clients
python deploy_client.py --setup client1 --name "Client 1 Corp"
python deploy_client.py --setup client2 --name "Client 2 LLC"
python deploy_client.py --setup agency --name "My Agency"

# Each client gets isolated:
# - configs/client1.yaml
# - credentials/client1/
# - tokens/client1/
# - deployments/client1/
```

#### Directory Structure After Setup
```
MCP SERVERS/
├── configs/
│   ├── client1.yaml
│   ├── client2.yaml
│   └── agency.yaml
├── credentials/
│   ├── client1/
│   │   └── gmail_credentials.json
│   ├── client2/
│   │   └── gmail_credentials.json
│   └── agency/
│       └── gmail_credentials.json
├── tokens/
│   ├── client1/
│   │   └── gmail_token.pickle
│   └── client2/
│       └── gmail_token.pickle
└── deployments/
    ├── client1/
    │   ├── docker-compose.yml
    │   ├── .env
    │   └── start.sh
    └── client2/
        ├── docker-compose.yml
        ├── .env
        └── start.sh
```

### 3. Configuration File Example

Each client gets a `configs/{client_id}.yaml` file:

```yaml
client_info:
  name: "Client 1 Corp"
  description: "Configuration for MCP servers"
  created: "2024-01-01"

gmail:
  credentials_path: "credentials/client1/gmail_credentials.json"
  token_path: "tokens/client1/gmail_token.pickle"
  scopes: ["https://www.googleapis.com/auth/gmail.modify"]

telegram:
  token: "your_client1_telegram_bot_token"
  chat_id: "your_client1_chat_id"
  parse_mode: "HTML"

pdf_tools:
  api_key: "your_client1_pdfshift_api_key"
  default_format: "A4"
  default_margin: 20

elevenlabs:
  api_key: "your_client1_elevenlabs_api_key"
  default_voice: "rachel"

supabase:
  url: "your_client1_supabase_url"
  key: "your_client1_supabase_key"
  table_prefix: "client1"

instagram:
  access_token: "your_client1_instagram_access_token"
  app_id: "your_facebook_app_id"
  app_secret: "your_facebook_app_secret"
  account_id: "your_instagram_business_account_id"
  page_id: "your_facebook_page_id"

tiktok:
  client_key: "your_tiktok_client_key"
  client_secret: "your_tiktok_client_secret"
  access_token: "your_tiktok_access_token"
  refresh_token: "your_tiktok_refresh_token"

calendar:
  timezone: "America/New_York"
  business_hours:
    start: "09:00"
    end: "17:00"
  excluded_days: ["saturday", "sunday"]
```

### 4. Running Servers for Different Clients

```bash
# List all configured clients
python deploy_client.py --list

# Run servers for a specific client
python deploy_client.py --run client1

# Stop servers for a client
python deploy_client.py --stop client1

# Or set client via environment variable
export MCP_CLIENT_ID=client2
python "Gmail MPC Server.py"
```

### 5. Docker Deployment (Production)

```bash
# Build the image
docker build -t mcp-servers .

# Run for different clients
docker run -d \
  --name mcp-gmail-client1 \
  -e MCP_CLIENT_ID=client1 \
  -v $(pwd)/configs:/app/configs \
  -v $(pwd)/credentials:/app/credentials \
  -v $(pwd)/tokens:/app/tokens \
  mcp-servers python "Gmail MPC Server.py"

# Or use docker-compose
cd deployments/client1
docker-compose up -d
```

### 6. Credential Setup

#### Gmail Authentication
1. Create a Google Cloud project
2. Enable Gmail API
3. Create OAuth2 credentials
4. Download `credentials.json` to `credentials/{client_id}/gmail_credentials.json`

#### Telegram Bot Setup
1. Message @BotFather on Telegram
2. Create a new bot with `/newbot`
3. Get your bot token
4. Add to config file or environment variables

#### Instagram/Meta Setup
1. Create a Facebook Developer account
2. Create a new Facebook App
3. Enable Instagram Basic Display or Instagram Graph API
4. Get your access token and app credentials
5. Connect your Instagram Business account
6. Add credentials to your config file

#### TikTok Setup
1. Create a TikTok for Developers account
2. Apply for TikTok API access (Login Kit or Content Posting API)
3. Create a TikTok app and get your client credentials
4. Obtain access tokens through OAuth flow
5. Add credentials to your config file
6. Note: Some features require TikTok Research API approval

#### API Keys
Add all API keys to the client configuration file or use environment variables with client prefix:
```bash
export CLIENT1_TELEGRAM_TOKEN=your_token
export CLIENT1_PDF_API_KEY=your_key
export CLIENT1_ELEVENLABS_API_KEY=your_key
export CLIENT1_INSTAGRAM_ACCESS_TOKEN=your_token
export CLIENT1_FACEBOOK_APP_ID=your_app_id
export CLIENT1_TIKTOK_CLIENT_KEY=your_tiktok_key
export CLIENT1_TIKTOK_ACCESS_TOKEN=your_tiktok_token
```

## 🔄 n8n Integration Examples

### Client-Specific Workflows

With the multi-client setup, you can create workflows that automatically use the right credentials:

```javascript
// In n8n, set the client context
const clientId = $env.CLIENT_ID || 'default';

// All MCP calls will use this client's configuration
```

### Example 1: Email-to-Calendar Workflow
```json
{
  "nodes": [
    {
      "name": "Gmail Trigger",
      "type": "Gmail",
      "parameters": {
        "operation": "search",
        "query": "subject:meeting OR subject:appointment"
      }
    },
    {
      "name": "Parse Date",
      "type": "MCP Calendar",
      "parameters": {
        "tool": "parse_natural_date",
        "date_string": "{{ $json.body }}"
      }
    },
    {
      "name": "Create Event",
      "type": "MCP Calendar", 
      "parameters": {
        "tool": "create_event",
        "title": "{{ $json.subject }}",
        "start_time": "{{ $json.datetime }}"
      }
    }
  ]
}
```

### Example 2: Instagram Content Automation
```json
{
  "nodes": [
    {
      "name": "Content Schedule Trigger",
      "type": "Cron",
      "parameters": {
        "expression": "0 14 * * *"
      }
    },
    {
      "name": "Get Supabase Content",
      "type": "MCP Supabase",
      "parameters": {
        "tool": "query",
        "table": "scheduled_posts",
        "filters": {"post_date": "today"}
      }
    },
    {
      "name": "Post to Instagram",
      "type": "MCP Instagram",
      "parameters": {
        "tool": "instagram_post_photo",
        "image_url": "{{ $json.image_url }}",
        "caption": "{{ $json.caption }}"
      }
    },
    {
      "name": "Get Performance Data",
      "type": "MCP Instagram",
      "parameters": {
        "tool": "instagram_get_insights",
        "period": "day"
      }
    },
    {
      "name": "Notify Team",
      "type": "MCP Telegram",
      "parameters": {
        "tool": "send_formatted_list",
        "title": "📸 Instagram Post Published",
        "items": [
          {
            "title": "Post ID",
            "description": "{{ $json.post_id }}"
          },
          {
            "title": "Reach",
            "description": "{{ $json.insights.reach }}"
          }
        ]
      }
    }
  ]
}
```

### Example 3: TikTok Trend Analysis
```json
{
  "nodes": [
    {
      "name": "Daily Trend Check",
      "type": "Cron",
      "parameters": {
        "expression": "0 10 * * *"
      }
    },
    {
      "name": "Get Trending Hashtags",
      "type": "MCP TikTok",
      "parameters": {
        "tool": "tiktok_get_trending_hashtags",
        "country_code": "US",
        "limit": 15
      }
    },
    {
      "name": "Analyze Top Hashtags",
      "type": "MCP TikTok",
      "parameters": {
        "tool": "tiktok_search_hashtags",
        "keyword": "{{ $json.trending_hashtags[0].hashtag }}",
        "period": 7
      }
    },
    {
      "name": "Get Content Insights",
      "type": "MCP TikTok",
      "parameters": {
        "tool": "tiktok_get_content_insights",
        "days_back": 7
      }
    },
    {
      "name": "Generate Trend Report",
      "type": "MCP PDF Tools",
      "parameters": {
        "tool": "create_invoice_pdf",
        "invoice_data": {
          "title": "TikTok Trend Report",
          "trending_hashtags": "{{ $json }}",
          "performance_insights": "{{ $json }}"
        }
      }
    },
    {
      "name": "Alert Team",
      "type": "MCP Telegram",
      "parameters": {
        "tool": "send_formatted_list",
        "title": "🔥 Daily TikTok Trends",
        "items": [
          {
            "title": "Top Trend",
            "description": "{{ $json.trending_hashtags[0].hashtag }}"
          },
          {
            "title": "Trend Score",
            "description": "{{ $json.trending_hashtags[0].trend_score }}"
          }
        ]
      }
    }
  ]
}
```

## 🌟 Advanced Workflow Ideas

1. **Smart Meeting Scheduler**
   - Gmail watches for meeting requests
   - Calendar finds available slots
   - Telegram sends confirmation to participants

2. **Social Media Content Pipeline**
   - Calendar triggers scheduled content
   - Instagram posts photos/videos
   - PDF generates performance reports
   - Gmail sends analytics to clients
   - Telegram notifies team of engagement

3. **Invoice Processing Pipeline**
   - PDF extracts invoice data
   - Supabase stores invoice records
   - Gmail sends confirmations
   - ElevenLabs creates voice summaries

4. **Multi-Platform Content Distribution**
   - Supabase stores content queue
   - Instagram posts visual content
   - Telegram distributes to channels
   - Gmail sends newsletters
   - PDF generates branded reports

5. **Automated Client Reporting**
   - Instagram pulls analytics data
   - PDF creates custom reports
   - Gmail sends to clients
   - Telegram notifies completion

6. **Hashtag Research & Strategy**
   - Instagram searches trending hashtags
   - Supabase stores performance data
   - Calendar schedules optimal posting times
   - ElevenLabs creates strategy briefings

7. **Cross-Platform Trend Analysis**
   - TikTok identifies trending hashtags
   - Instagram analyzes similar trends
   - PDF creates trend reports
   - Telegram alerts team to opportunities

8. **Multi-Platform Content Strategy**
   - TikTok provides trending insights
   - Calendar schedules optimal posting across platforms
   - Instagram handles visual content
   - PDF generates strategy reports
   - Gmail sends insights to clients

## 🔧 Development Guidelines

### Error Handling Pattern
All servers use consistent error handling:
```python
{
    "success": True/False,
    "data": {...},
    "error": "Error message if failed"
}
```

### Async Best Practices
- All operations are async
- Use `httpx.AsyncClient()` for HTTP requests
- Proper connection cleanup

### Security Considerations
- Environment variables for all secrets
- OAuth2 for secure API access
- Input validation and sanitization

## 📈 Monitoring & Debugging

Each server includes:
- Detailed error messages
- Timestamp tracking
- Operation logging
- Health check endpoints

## 🤝 Contributing

When adding new servers:
1. Follow the existing async patterns
2. Include comprehensive error handling
3. Add proper documentation
4. Update requirements.txt
5. Create n8n workflow examples

## 🚀 Advanced Usage Patterns

### Client Isolation Benefits
- **Security**: Each client's credentials are completely isolated
- **Scaling**: Add new clients without affecting existing ones
- **Customization**: Different settings per client (timezones, business hours, etc.)
- **Billing**: Track usage per client for service billing

### Environment Variable Patterns
```bash
# Development
export MCP_CLIENT_ID=dev
python "Gmail MPC Server.py"

# Production client 1
export MCP_CLIENT_ID=client1
python "Gmail MPC Server.py"

# Production client 2 with overrides
export MCP_CLIENT_ID=client2
export CLIENT2_TELEGRAM_TOKEN=special_token
python "Telegram MPC Server.py"
```

### Service Provider Setup
If you're building automation services for clients:

1. **Initial Setup**
```bash
python deploy_client.py --setup client_awesome_corp --name "Awesome Corp"
```

2. **Customize Configuration**
Edit `configs/client_awesome_corp.yaml` with their specific:
- API keys
- Business hours
- Timezone preferences
- Custom settings

3. **Deploy & Monitor**
```bash
python deploy_client.py --run client_awesome_corp
python deploy_client.py --list  # Check status
```

4. **Scale Operations**
- Each client runs in isolation
- Easy to add new clients
- Simple credential management
- Independent scaling per client

## 💰 Business Model Ideas

This complete social media automation setup enables powerful business models:

### Social Media Management
1. **Multi-Platform Management**: Instagram + TikTok automation for brands
2. **Trend Analysis Service**: Daily/weekly trend reports across platforms
3. **Content Strategy Optimization**: Data-driven hashtag and timing recommendations
4. **Automated Reporting**: Client dashboards with cross-platform analytics

### Agency Services
1. **Full-Service Social Media Automation**: End-to-end management
2. **Influencer Analytics Platform**: Performance tracking across platforms
3. **Brand Monitoring & Insights**: Trend analysis and competitive intelligence
4. **Content Scheduling & Optimization**: Peak time posting with trend integration

### SaaS Opportunities
1. **White-label Social Media Dashboard**: Rebrand and sell to agencies
2. **Trend Analysis API**: Sell trend data to businesses
3. **Content Optimization Tool**: Hashtag and timing recommendations
4. **Multi-Client Management Platform**: Agency-focused automation platform

### Revenue Streams
- **Monthly subscriptions**: $200-2000/month per client
- **Custom automation**: $5,000-25,000 setup fees
- **API access**: $0.10-1.00 per API call
- **Premium analytics**: $500-5,000/month enterprise plans

## 📄 License

MIT License - Feel free to use and modify for your automation needs!
