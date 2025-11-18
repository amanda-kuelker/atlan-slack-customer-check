# Atlan Health Checker - Netlify Serverless

Professional data governance assessments via Slack commands. Generates industry-specific health reports with actionable recommendations.

## 🚀 Quick Deploy to Netlify

### 1. Repository Setup
```bash
# Clone this repo or create new one with these files
git init
git add .
git commit -m "Initial Atlan Health Checker"
git branch -M main
git remote add origin https://github.com/yourusername/atlan-health-checker.git
git push -u origin main
```

### 2. Deploy to Netlify
1. Go to [netlify.com](https://netlify.com)
2. "New site from Git"
3. Connect your GitHub repo
4. Deploy (uses `netlify.toml` config automatically)

### 3. Configure Slack App
1. Create Slack app at [api.slack.com](https://api.slack.com/apps)
2. Add Slash Command:
   - **Command:** `/atlan-health`
   - **Request URL:** `https://your-site.netlify.app/slack/atlan-setup`
   - **Method:** POST
3. Install app to workspace

## 📋 Usage

### Basic Command
```bash
/atlan-health "Company Name" https://tenant.atlan.com
```

### With Industry & Filters
```bash
/atlan-health "DPR Construction" https://dpr.atlan.com industry:construction tags:Safety,OSHA
```

### Supported Industries
- `construction` 🏗️ - Project management, financials, operations
- `healthcare` 🏥 - Patient data, clinical systems, compliance  
- `finance` 🏦 - Trading, risk management, regulatory reporting
- `manufacturing` 🏭 - Production data, quality control, supply chain
- `retail` 🛍️ - Customer data, inventory, sales analytics
- `technology` 💻 - User data, product analytics, performance metrics

### Filter Options
- `industry:construction` - Set specific industry analysis
- `tags:Safety,OSHA` - Filter by asset tags
- `connections:snowflake` - Filter by connection type
- `certificate:VERIFIED` - Filter by certification status

## 📊 Sample Output

```
🏗️ DPR Construction - Data Governance Assessment

Prepared by Atlan Professional Services | November 18, 2025

🔴 Governance Health Score: 23/100 - Project Risk

📊 Current State Analysis
Assessment based on 150 key datasets across project management, financials, and operations

* 📝 Documentation: 12.0% (18/150 datasets documented)
* 👥 Data Ownership: 8.0% (12 datasets with clear owners)
* ✅ Data Certification: 6.0% (9 datasets verified)
* 🏗️ Business Context: 4.0% (6 datasets with context)

🎯 Strategic Recommendations for DPR Construction

1. 🚨 Data Discovery Crisis (CRITICAL Priority)
Expected ROI: $200K+ annual savings

2. ⚡ Data Accountability Gap (HIGH Priority)  
Expected ROI: 25% faster issue resolution

3. ⚠️ Data Trust & Compliance (MEDIUM Priority)
Expected ROI: Reduced compliance risk

📈 30-60-90 Day Construction & Engineering Roadmap
💰 Business Impact Analysis
🚀 Immediate Next Steps
```

## 🔧 How It Works

1. **Single Function**: One Python function handles all requests
2. **Industry Detection**: Automatically detects industry from company name or explicit filter
3. **Realistic Data**: Generates industry-appropriate mock data for assessments
4. **Health Scoring**: Weighted algorithm (Documentation 30%, Ownership 25%, Certification 25%, Context 20%)
5. **Professional Output**: Canvas-style assessments with specific recommendations

## 🏗️ Architecture

```
netlify/
└── functions/
    └── health.py          # Single serverless function
netlify.toml               # Build configuration  
_redirects                 # URL routing
requirements.txt           # Dependencies (empty - stdlib only)
README.md                  # This file
```

## 📈 Features

- ✅ **Zero Dependencies** - Uses Python standard library only
- ✅ **Industry-Specific** - Tailored analysis for 6+ industries
- ✅ **Professional Output** - Canvas-style reports with actionable insights
- ✅ **Slack Integration** - Native slash command support
- ✅ **Web Interface** - Works in browser for demos
- ✅ **Error Handling** - Graceful fallbacks and user-friendly messages
- ✅ **Fast Deployment** - Single function, minimal configuration

## 🧪 Testing

### Test in Browser
Visit your Netlify URL to see demo assessment

### Test Slack Commands
```bash
# Help
/atlan-health

# Basic assessment
/atlan-health "TestCorp" https://test.atlan.com

# Construction example
/atlan-health "DPR Construction" https://dpr.atlan.com industry:construction tags:Safety,OSHA

# Healthcare example  
/atlan-health "Regional Hospital" https://health.atlan.com industry:healthcare tags:PHI,HIPAA

# Finance example
/atlan-health "MegaBank" https://bank.atlan.com industry:finance tags:PII,SOX
```

## 🔄 Future Enhancements

When ready to integrate with real Atlan data:

1. Add MCP (Model Context Protocol) integration
2. Connect to actual Atlan tenant APIs
3. Real-time data fetching and analysis
4. Historical health tracking
5. Team collaboration features

## 🆘 Troubleshooting

### Deployment Issues
- Ensure `netlify.toml` is in root directory
- Check Python runtime is set to 3.8
- Verify function is in `netlify/functions/` directory

### Slack Issues  
- Confirm Request URL points to your Netlify domain
- Check Slack app has proper permissions
- Verify slash command is configured correctly

### Testing
- Browser test: Visit your Netlify URL directly
- Slack test: Use `/atlan-health` with no parameters to see help

## 📞 Support

This is a self-contained solution using Python standard library only. No external dependencies or complex setup required!

Ready to generate professional data governance assessments! 🎯
