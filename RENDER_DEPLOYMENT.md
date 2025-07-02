# 🚀 Render Deployment Guide

Your MCP servers are now **100% ready** for Render deployment! This guide will get you up and running in production.

## 📋 **Pre-deployment Checklist**

✅ All 8 MCP servers are complete and Render-ready  
✅ `render.yaml` configuration file is set up  
✅ Environment variables template is ready  
✅ Servers automatically detect Render environment  
✅ Port binding is configured for Render's requirements  

## 🛠️ **Deployment Methods**

### **Option 1: Deploy via GitHub (Recommended)**

1. **Push to GitHub Repository**:
```bash
# Initialize git if not already done
git init
git add .
git commit -m "Complete MCP server collection for Render"
git remote add origin https://github.com/yourusername/mcp-servers.git
git push -u origin main
```

2. **Connect to Render**:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`

3. **Configure Environment Variables** (see section below)

### **Option 2: Deploy Individual Services**

If you want to deploy services individually:

1. **Go to Render Dashboard**
2. **Click "New" → "Web Service"**
3. **Connect your repository**
4. **Configure each service**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python "Calendar MCP Server.py"` (for Calendar server)
   - **Environment**: `Python 3`
   - **Plan**: `Starter` (free tier)

## 🔐 **Environment Variables Setup**

### **Step 1: Set Core Variables**

For **ALL services**, add these environment variables in Render:

```bash
RENDER=true
MCP_CLIENT_ID=production
```

### **Step 2: Service-Specific Variables**

Copy the relevant variables from `render-env-template.txt` for each service you're deploying.

#### **🗓️ Calendar Server** (No API keys needed!)
```bash
CALENDAR_TIMEZONE=UTC
```

#### **💬 Telegram Server**
```bash
PRODUCTION_TELEGRAM_TOKEN=123456789:ABCDEF...
PRODUCTION_TELEGRAM_CHAT_ID=123456789
```

#### **📸 Instagram Server**
```bash
PRODUCTION_INSTAGRAM_ACCESS_TOKEN=IGQVJXeW5...
PRODUCTION_FACEBOOK_APP_ID=123456789
PRODUCTION_FACEBOOK_APP_SECRET=abc123...
PRODUCTION_INSTAGRAM_ACCOUNT_ID=17841400455970203
PRODUCTION_FACEBOOK_PAGE_ID=123456789
```

#### **🎵 TikTok Server**
```bash
PRODUCTION_TIKTOK_CLIENT_KEY=aw123...
PRODUCTION_TIKTOK_CLIENT_SECRET=abc123...
PRODUCTION_TIKTOK_ACCESS_TOKEN=act.123...
PRODUCTION_TIKTOK_REFRESH_TOKEN=rft.123...
```

#### **📄 PDF Tools Server**
```bash
PRODUCTION_PDF_API_KEY=sk_daa4548ae0975a72b71cd257110838531d8db8f1
```

#### **🎤 ElevenLabs Server**
```bash
PRODUCTION_ELEVENLABS_API_KEY=sk_123...
PRODUCTION_ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM
```

#### **🗄️ Supabase Server**
```bash
PRODUCTION_SUPABASE_URL=https://abc.supabase.co
PRODUCTION_SUPABASE_KEY=eyJhbGc...
```

#### **☁️ Dropbox Server**
```bash
PRODUCTION_DROPBOX_ACCESS_TOKEN=sl.B123...
PRODUCTION_DROPBOX_REFRESH_TOKEN=abc123...
PRODUCTION_DROPBOX_APP_KEY=abc123...
PRODUCTION_DROPBOX_APP_SECRET=abc123...
```

## 🌍 **Service URLs After Deployment**

Once deployed, your services will be available at:

- **Calendar**: `https://calendar-mcp-server.onrender.com`
- **Telegram**: `https://telegram-mcp-server.onrender.com`
- **Instagram**: `https://instagram-mcp-server.onrender.com`
- **TikTok**: `https://tiktok-mcp-server.onrender.com`
- **PDF Tools**: `https://pdf-tools-mcp-server.onrender.com`
- **ElevenLabs**: `https://elevenlabs-mcp-server.onrender.com`
- **Supabase**: `https://supabase-mcp-server.onrender.com`
- **Dropbox**: `https://dropbox-mcp-server.onrender.com`

## 📱 **Testing Your Deployed Services**

### **1. Health Check**
Visit any service URL - you should see the MCP server running.

### **2. Test with n8n**
Use the service URLs as webhook endpoints in your n8n workflows.

### **3. Test Individual Tools**
```bash
# Example: Test calendar service
curl -X POST https://calendar-mcp-server.onrender.com/api/tools \
  -H "Content-Type: application/json" \
  -d '{"tool": "create_event", "params": {"title": "Test Meeting", "start_time": "tomorrow at 2pm"}}'
```

## 🔧 **Configuration Tips**

### **Free Tier Optimization**
- Services on free tier sleep after 15 minutes of inactivity
- They wake up automatically when called (takes ~30 seconds)
- Consider upgrading to Starter plan ($7/month) for always-on services

### **Resource Management**
- Each service runs independently
- Start with the services you need most
- Scale up as your usage grows

### **Environment Management**
- Use `production` as your client_id for all Render deployments
- Keep local configs separate from production configs
- Store sensitive credentials only in Render environment variables

## 🚨 **Troubleshooting**

### **Service Won't Start**
1. **Check Build Logs**: Look for missing dependencies
2. **Verify Environment Variables**: Ensure all required variables are set
3. **Check Python Version**: Render uses Python 3.x by default

### **Service Times Out**
1. **Check if it's sleeping**: Free tier services sleep after 15 minutes
2. **Verify PORT binding**: Services must listen on `$PORT` environment variable
3. **Check startup time**: Large dependencies can take time to load

### **API Errors**
1. **Verify credentials**: Check all API keys and tokens
2. **Check rate limits**: Some APIs have usage limits
3. **Validate configurations**: Ensure all required fields are set

### **Common Issues & Solutions**

#### **"Module not found" Error**
```bash
# Solution: Add missing dependency to requirements.txt
echo "missing-package>=1.0.0" >> requirements.txt
```

#### **"Port already in use"**
```bash
# Solution: Render automatically sets PORT - don't hardcode it
port = int(os.getenv("PORT", 8000))  # ✅ Correct
port = 8000  # ❌ Don't do this
```

#### **"Authentication failed"**
```bash
# Solution: Check environment variable names
# They must exactly match the format: PRODUCTION_{SERVICE}_{SETTING}
PRODUCTION_TELEGRAM_TOKEN  # ✅ Correct
TELEGRAM_TOKEN            # ❌ Won't work in production
```

## 📈 **Scaling for Production**

### **Performance Optimization**
1. **Enable caching** for frequently accessed data
2. **Use connection pooling** for database connections
3. **Implement rate limiting** to prevent API abuse

### **Monitoring**
1. **Use Render's built-in monitoring**
2. **Set up health checks** for critical services
3. **Monitor API usage** to avoid rate limits

### **Security**
1. **Never commit API keys** to version control
2. **Use environment variables** for all secrets
3. **Implement proper error handling** to avoid exposing internal details

## 💰 **Cost Estimation**

### **Free Tier** (Good for testing)
- ✅ 750 hours/month per service
- ✅ Services sleep after 15 minutes
- ❌ Limited compute resources

### **Starter Plan** ($7/month per service)
- ✅ Always-on services
- ✅ More compute resources
- ✅ Better performance

### **For Production Usage**
- **Start**: Deploy 2-3 key services on free tier
- **Scale**: Move to Starter plan for critical services
- **Optimize**: Use multiple services efficiently

## 🎯 **Next Steps**

1. **Deploy Calendar & PDF servers first** (no API keys needed)
2. **Add Telegram for notifications**
3. **Deploy other services as you get API credentials**
4. **Connect to n8n workflows**
5. **Monitor usage and scale as needed**

## 🏆 **Production Ready!**

Your MCP server collection is now **enterprise-ready** and can handle:
- **Multiple clients** with isolated configurations
- **High availability** with Render's infrastructure
- **Automatic scaling** based on demand
- **Professional APIs** for automation workflows

Ready to build the next generation of automation services! 🚀 