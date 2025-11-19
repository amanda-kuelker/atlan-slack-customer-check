import json
import re
import random
import urllib.parse
from datetime import datetime

def handler(event, context):
    """Single Netlify function for Atlan health assessments"""
    
    try:
        # Add debug logging
        print(f"Event: {json.dumps(event, indent=2)}")
        
        # Handle CORS preflight
        if event.get('httpMethod') == 'OPTIONS':
            return cors_response()
        
        # Get request body
        body = event.get('body', '')
        if event.get('isBase64Encoded'):
            import base64
            body = base64.b64decode(body).decode('utf-8')
        
        print(f"Request body: {body}")
        
        # Check if this is a Slack request (has form data with token)
        is_slack = body and 'token=' in body
        print(f"Is Slack request: {is_slack}")
        
        if is_slack:
            return handle_slack_command(body)
        else:
            return handle_web_request()
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return error_response(f"Service error: {str(e)}")

def handle_slack_command(body):
    """Process Slack slash command"""
    try:
        # Parse form data
        form_data = urllib.parse.parse_qs(body)
        command_text = form_data.get('text', [''])[0].strip()
        user_name = form_data.get('user_name', ['user'])[0]
        
        print(f"Slack command from {user_name}: {command_text}")
        
        # Show help if empty
        if not command_text:
            return slack_response(get_help_text(), ephemeral=True)
        
        # Parse and generate assessment
        parsed = parse_command(command_text)
        if not parsed:
            return slack_response("❌ Please include a company name", ephemeral=True)
        
        assessment = generate_assessment(
            parsed['company_name'],
            parsed.get('atlan_url'),
            parsed.get('filters', {})
        )
        
        # Format for Slack (with length limit)
        if len(assessment) > 3500:
            assessment = assessment[:3500] + "\n\n...Assessment truncated for Slack display"
        
        return slack_response(f"📋 **Assessment Complete**\n\n```\n{assessment}\n```")
        
    except Exception as e:
        print(f"Slack handler error: {str(e)}")
        return slack_response(f"❌ Error processing command: {str(e)}", ephemeral=True)

def handle_web_request():
    """Handle web browser requests - show demo"""
    demo_content = """🏗️ DPR Construction - Data Governance Assessment

Prepared by Atlan Professional Services | November 18, 2025

🔴 Governance Health Score: 23/100 - Project Risk

📊 Current State Analysis
Assessment based on 150 key datasets across project management, financials, and operations

* 📝 Project Documentation: 12.0% (18/150 datasets documented)
* 👥 Data Ownership: 8.0% (12 datasets with clear owners)
* ✅ Data Certification: 6.0% (9 datasets verified)
* 🏗️ Business Context: 4.0% (6 datasets with context)

🎯 Strategic Recommendations

1. 🚨 Project Data Discovery Crisis (CRITICAL)
   Expected ROI: $200K+ annual savings

2. ⚡ Data Accountability Gap (HIGH Priority)
   Expected ROI: 25% faster issue resolution

3. ⚠️ Data Trust & Compliance (MEDIUM Priority)
   Expected ROI: Reduced compliance risk

📈 30-60-90 Day Roadmap
30 Days: Document critical datasets → Target: 43/100
60 Days: Implement workflows → Target: 58/100
90 Days: Achieve maturity → Target: 73/100

💰 Business Impact: $500K+ annual efficiency gains

🚀 Ready to unlock your data's potential?

---
To use via Slack: /atlan-health "Company Name" https://tenant.atlan.com
"""
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain',
            'Access-Control-Allow-Origin': '*'
        },
        'body': demo_content
    }

def parse_command(text):
    """Parse company name, URL, and filters from command text"""
    if not text:
        return None
    
    # Handle quoted company names
    if text.startswith('"'):
        end_quote = text.find('"', 1)
        if end_quote != -1:
            company = text[1:end_quote]
            remaining = text[end_quote + 1:].strip()
        else:
            parts = text.split()
            company = parts[0].strip('"')
            remaining = ' '.join(parts[1:])
    else:
        parts = text.split()
        company = parts[0]
        remaining = ' '.join(parts[1:]) if len(parts) > 1 else ''
    
    # Extract URL
    url = None
    url_pattern = r'https?://[\w\.-]+\.atlan\.com[^\s]*'
    url_match = re.search(url_pattern, remaining)
    if url_match:
        url = url_match.group(0)
        remaining = remaining.replace(url, '').strip()
    
    # Parse filters like industry:construction tags:Safety,OSHA
    filters = {}
    filter_pattern = r'(\w+):([\w,.-]+)'
    for match in re.finditer(filter_pattern, remaining):
        key = match.group(1)
        value = match.group(2)
        filters[key] = value.split(',') if ',' in value else value
    
    return {
        'company_name': company,
        'atlan_url': url,
        'filters': filters
    }

def detect_industry(company_name, filters):
    """Detect industry from name and filters"""
    if 'industry' in filters:
        specified = filters['industry']
        if isinstance(specified, list):
            specified = specified[0]
        return specified.lower()
    
    name = company_name.lower()
    
    # Industry keywords
    if any(word in name for word in ['health', 'medical', 'hospital', 'pharma']):
        return 'healthcare'
    if any(word in name for word in ['bank', 'financial', 'capital', 'credit']):
        return 'finance'
    if any(word in name for word in ['construction', 'building', 'engineering']):
        return 'construction'
    if any(word in name for word in ['retail', 'store', 'shop', 'commerce']):
        return 'retail'
    if any(word in name for word in ['manufacturing', 'factory', 'industrial']):
        return 'manufacturing'
    
    return 'technology'

def generate_mock_data(industry):
    """Generate realistic data based on industry"""
    base_ranges = {
        'construction': {'total': (120, 180), 'doc': 0.12, 'own': 0.08, 'cert': 0.06, 'tag': 0.40},
        'healthcare': {'total': (200, 300), 'doc': 0.25, 'own': 0.15, 'cert': 0.20, 'tag': 0.60},
        'finance': {'total': (150, 250), 'doc': 0.30, 'own': 0.20, 'cert': 0.25, 'tag': 0.55},
        'manufacturing': {'total': (130, 220), 'doc': 0.18, 'own': 0.12, 'cert': 0.15, 'tag': 0.45},
        'retail': {'total': (100, 180), 'doc': 0.22, 'own': 0.14, 'cert': 0.18, 'tag': 0.50},
        'technology': {'total': (90, 160), 'doc': 0.35, 'own': 0.25, 'cert': 0.30, 'tag': 0.65}
    }
    
    config = base_ranges.get(industry, base_ranges['technology'])
    total = random.randint(*config['total'])
    
    return {
        'total_assets': total,
        'documented_assets': int(total * config['doc']),
        'owned_assets': int(total * config['own']),
        'verified_assets': int(total * config['cert']),
        'tagged_assets': int(total * config['tag'])
    }

def calculate_health_score(industry, data):
    """Calculate weighted health score"""
    total = data['total_assets']
    if total == 0:
        return {'overall_score': 0, 'documentation_pct': 0, 'ownership_pct': 0, 'certification_pct': 0, 'context_pct': 0}
    
    # Calculate percentages
    doc_pct = (data['documented_assets'] / total) * 100
    own_pct = (data['owned_assets'] / total) * 100
    cert_pct = (data['verified_assets'] / total) * 100
    tag_pct = (data['tagged_assets'] / total) * 100
    
    # Weighted score: Documentation 30%, Ownership 25%, Certification 25%, Context 20%
    score = (doc_pct * 0.3 + own_pct * 0.25 + cert_pct * 0.25 + tag_pct * 0.2)
    
    # Industry multipliers (stricter industries get lower scores)
    multipliers = {
        'healthcare': 0.80,
        'finance': 0.85,
        'construction': 0.90,
        'manufacturing': 0.87,
        'retail': 0.88,
        'technology': 0.92
    }
    
    final_score = int(score * multipliers.get(industry, 0.90))
    
    return {
        'overall_score': final_score,
        'documentation_pct': doc_pct,
        'ownership_pct': own_pct,
        'certification_pct': cert_pct,
        'context_pct': tag_pct
    }

def generate_assessment(company_name, atlan_url, filters):
    """Generate complete professional assessment"""
    industry = detect_industry(company_name, filters)
    data = generate_mock_data(industry)
    scores = calculate_health_score(industry, data)
    
    # Industry configurations
    industries = {
        'construction': {'name': 'Construction & Engineering', 'icon': '🏗️', 'focus': 'project management, financials, and operations'},
        'healthcare': {'name': 'Healthcare & Life Sciences', 'icon': '🏥', 'focus': 'patient data, clinical systems, and compliance'},
        'finance': {'name': 'Financial Services', 'icon': '🏦', 'focus': 'trading, risk management, and regulatory reporting'},
        'manufacturing': {'name': 'Manufacturing & Industrial', 'icon': '🏭', 'focus': 'production data, quality control, and supply chain'},
        'retail': {'name': 'Retail & Consumer', 'icon': '🛍️', 'focus': 'customer data, inventory, and sales analytics'},
        'technology': {'name': 'Technology & Software', 'icon': '💻', 'focus': 'user data, product analytics, and performance metrics'}
    }
    
    info = industries.get(industry, industries['technology'])
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # Health category
    score = scores['overall_score']
    if score < 30:
        category, emoji = "Project Risk", "🔴"
    elif score < 60:
        category, emoji = "Moderate Risk", "🟡" 
    elif score < 80:
        category, emoji = "Good Foundation", "🟢"
    else:
        category, emoji = "Excellence", "🌟"
    
    return f"""{info['icon']} {company_name} - Data Governance Assessment

Prepared by Atlan Professional Services | {current_date}

{emoji} Governance Health Score: {score}/100 - {category}

📊 Current State Analysis
Assessment based on {data['total_assets']} key datasets across {info['focus']}

* 📝 Documentation: {scores['documentation_pct']:.1f}% ({data['documented_assets']}/{data['total_assets']} datasets documented)
* 👥 Data Ownership: {scores['ownership_pct']:.1f}% ({data['owned_assets']} datasets with clear owners)
* ✅ Data Certification: {scores['certification_pct']:.1f}% ({data['verified_assets']} datasets verified)
* 🏗️ Business Context: {scores['context_pct']:.1f}% ({data['tagged_assets']} datasets with context)

🎯 Strategic Recommendations for {company_name}

1. 🚨 Data Discovery Crisis (CRITICAL Priority)
At {scores['documentation_pct']:.1f}% documentation, teams waste hours searching for reliable data.
Expected ROI: $200K+ annual savings in operational efficiency

2. ⚡ Data Accountability Gap (HIGH Priority)  
With {scores['ownership_pct']:.1f}% ownership, no clear escalation path when data issues occur.
Expected ROI: 25% faster issue resolution

3. ⚠️ Data Trust & Compliance (MEDIUM Priority)
Only {scores['certification_pct']:.1f}% certified data means teams don't know which data is reliable.
Expected ROI: Reduced compliance risk, improved decision confidence

📈 30-60-90 Day {info['name']} Roadmap

30 Days: Foundation Building
* Document critical {industry} datasets
* Assign data owners to high-priority areas
* Target Health Score: {min(score + 20, 100)}/100

60 Days: Process Optimization
* Implement automated governance workflows  
* Train teams on data best practices
* Target Health Score: {min(score + 35, 100)}/100

90 Days: Competitive Advantage
* Achieve industry-leading governance maturity
* Demonstrate measurable ROI to leadership
* Target Health Score: {min(score + 50, 100)}/100

💰 Business Impact for {company_name}

Current Costs:
* Teams spend 2+ hours daily finding reliable data
* Data quality issues delay critical decisions
* Manual processes cost ~$150K annually

Target Benefits:
* 75% reduction in data discovery time
* Faster decision making with trusted data
* $400K+ annual efficiency gains

🚀 Immediate Next Steps

Week 1: Leadership alignment on data governance priority
Week 2: Document pilot process datasets
This Quarter: Scale governance practices across all critical processes

Ready to unlock your data's potential? Let's start with your highest-impact processes first."""

def get_help_text():
    """Return help text for empty commands"""
    return """🏥 **Atlan Professional Health Check**

📋 **Usage:**
`/atlan-health "Company Name" https://tenant.atlan.com industry:construction tags:Safety,OSHA`

🎯 **Industries:** finance, healthcare, construction, retail, technology, manufacturing
🔍 **Filters:** industry, tags, connections, certificate

📝 **Examples:**
`/atlan-health "DPR Construction" https://dpr.atlan.com industry:construction`
`/atlan-health "Regional Hospital" https://health.atlan.com industry:healthcare tags:PHI,HIPAA`
`/atlan-health "TechCorp" https://tech.atlan.com industry:technology`"""

def slack_response(text, ephemeral=False):
    """Format response for Slack"""
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            "response_type": "ephemeral" if ephemeral else "in_channel",
            "text": text
        })
    }

def cors_response():
    """Handle CORS preflight requests"""
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
        },
        'body': ''
    }

def error_response(message):
    """Return error response"""
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            "response_type": "ephemeral",
            "text": f"❌ {message}"
        })
    }
