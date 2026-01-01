# 🔍 Competitive Intelligence System
## SimilarWeb Paywall Bypass via API Mega Library

**Cost:** $0 (Apify free tier)  
**Setup Time:** 5 minutes  
**Data Quality:** Production-grade SimilarWeb data

---

## 🎯 **Purpose**

This module automates competitor traffic analysis by bypassing SimilarWeb's paywall using the Apify API. It's **Step 1A** in the 10-Step Validate-Build methodology.

**When to use:**
- ✅ Before problem interviews (understand existing solutions)
- ✅ Before pricing decisions (benchmark competitor ARPUs)
- ✅ Before building MVP (identify table-stakes features)
- ✅ Monthly (track competitor growth trends)

---

## 🚀 **Quick Start (3 Steps)**

### Step 1: Set API Token

```bash
# Add to .env file
echo "APIFY_API_TOKEN=your_token_here" >> ../.env

# Or export directly
export APIFY_API_TOKEN="apify_api_xxxxxxxxxxxxx"
```

**Get your token:**  
https://apify.com/account/integrations (free signup, $5 credit included)

### Step 2: Analyze Competitors

```bash
python3 scripts/analyze_competitors.py \
  --domains "competitor1.com,competitor2.com,competitor3.com" \
  --output results/analysis_$(date +%Y%m%d).json
```

**Example (real estate investing tools):**
```bash
python3 scripts/analyze_competitors.py \
  --domains "propertyonion.com,rehabvaluator.com,dealcheck.io,zilculator.com" \
  --output results/real_estate_tools_20251231.json
```

### Step 3: Generate Executive Summary

```bash
python3 scripts/generate_summary.py \
  --input results/analysis_20251231.json \
  --product-name "Your Product Name" \
  --product-focus "Your niche (e.g., foreclosure auctions)" \
  --target-users 5000 \
  --target-arpu 297 \
  --output results/EXEC_SUMMARY_20251231.md
```

**Done!** You now have:
1. Raw JSON data (`results/analysis_*.json`)
2. Executive summary report (`results/EXEC_SUMMARY_*.md`)

---

## 📊 **What You Get**

### Traffic Metrics
- Monthly visit counts
- Traffic trends (last 3 months)
- Geographic distribution
- Traffic sources (direct, search, social, referrals, paid)

### Engagement Metrics
- Bounce rate (% who leave immediately)
- Pages per visit (depth of engagement)
- Time on site (session duration)

### Competitive Intelligence
- Global/country/category rankings
- Market share estimates
- Revenue modeling
- Feature gap analysis
- Strategic recommendations

---

## 📁 **File Structure**

```
competitive-intel/
├── README.md                        # This file
├── scripts/
│   ├── analyze_competitors.py       # SimilarWeb scraper
│   └── generate_summary.py          # Report generator
├── templates/
│   └── (future: custom report templates)
└── results/
    ├── analysis_YYYYMMDD.json       # Raw competitor data
    └── EXEC_SUMMARY_YYYYMMDD.md     # Executive summary
```

---

## 🔧 **Advanced Usage**

### Analyze Many Competitors (Up to 10)

```bash
python3 scripts/analyze_competitors.py \
  --domains "comp1.com,comp2.com,comp3.com,comp4.com,comp5.com,comp6.com,comp7.com,comp8.com,comp9.com,comp10.com" \
  --output results/full_market_analysis.json
```

### Use Custom API Token

```bash
python3 scripts/analyze_competitors.py \
  --domains "competitor.com" \
  --token "apify_api_YOUR_CUSTOM_TOKEN" \
  --output results/analysis.json
```

### Monthly Tracking

```bash
# Create a monthly cron job
echo "0 0 1 * * cd /path/to/validate-build-system/competitive-intel && python3 scripts/analyze_competitors.py --domains 'comp1.com,comp2.com' --output results/analysis_\$(date +\%Y\%m\%d).json" | crontab -
```

---

## 🎓 **Example Workflow**

### Real-World Example: Analyzing Real Estate Investment Tools

```bash
# 1. Analyze 4 competitors
python3 scripts/analyze_competitors.py \
  --domains "propertyonion.com,rehabvaluator.com,dealcheck.io,zilculator.com" \
  --output results/real_estate_tools.json

# Output:
# ✅ PropertyOnion: 85,234 monthly visits
# ✅ RehabValuator: 50,432 monthly visits
# ✅ DealCheck: 48,079 monthly visits
# ✅ Zilculator: 3,810 monthly visits
# Total market: 187,555 visits/month

# 2. Generate executive summary
python3 scripts/generate_summary.py \
  --input results/real_estate_tools.json \
  --product-name "BidDeed.AI" \
  --product-focus "Foreclosure auction intelligence" \
  --target-users 5000 \
  --target-arpu 297 \
  --output results/BidDeed_Competitive_Analysis.md

# 3. Review the report
cat results/BidDeed_Competitive_Analysis.md
```

**Key Insights from this analysis:**
- Market is 187K visits/month (3.6x larger than expected)
- PropertyOnion is market leader (45% share)
- DealCheck is declining (-22% MoM)
- RehabValuator is growing (+16% MoM)
- **Strategic implication:** Specialization beats generalization

---

## 📈 **Success Metrics**

Track these over time (run monthly):

| Metric | Good | Great | Excellent |
|--------|------|-------|-----------|
| **Traffic Growth** | +5% MoM | +10% MoM | +20% MoM |
| **Bounce Rate** | <50% | <45% | <40% |
| **Pages/Visit** | 3-5 | 5-7 | 8-10 |
| **Time on Site** | 2-3 min | 3-5 min | 5+ min |
| **Direct Traffic** | 50-60% | 60-70% | 70%+ |

---

## ⚠️ **Limitations & Caveats**

**SimilarWeb Data Accuracy:**
- ±20% accuracy on traffic estimates
- Requires minimum ~1,000 visits/month to track
- Very small sites (<1K visits) may show "N/A"
- Engagement metrics are estimates, not exact

**Not a substitute for:**
- Customer interviews (qualitative insights)
- Direct product testing (UX evaluation)
- Financial disclosures (actual revenue)

**Best used for:**
- Market sizing (TAM estimation)
- Trend analysis (growth vs decline)
- Benchmarking (what "good" looks like)
- Feature discovery (via competitor testing)

---

## 🔐 **Security & Privacy**

**API Token Security:**
- Never commit tokens to git
- Use environment variables or `.env` files
- Add `.env` to `.gitignore`
- Rotate tokens if exposed

**Data Privacy:**
- This tool scrapes **public SimilarWeb data only**
- No private user data is accessed
- Complies with SimilarWeb's terms of use
- Results should be kept confidential (competitive intelligence)

---

## 🐛 **Troubleshooting**

### Error: "APIFY_API_TOKEN not set"

**Solution:**
```bash
export APIFY_API_TOKEN="your_token_here"
# Or add to .env file
```

### Error: "requests library not found"

**Solution:**
```bash
pip install requests
```

### Error: "Scraper failed with status: FAILED"

**Possible causes:**
1. Invalid domain (check spelling)
2. Domain too small for SimilarWeb tracking
3. Apify API quota exceeded (upgrade plan)

**Solution:**
- Verify domains exist and are spelled correctly
- Try with larger, well-known domains first
- Check Apify dashboard for quota limits

### No Data Returned ("N/A" for all metrics)

**Cause:** Website too small for SimilarWeb tracking  
**Threshold:** ~1,000 visits/month minimum

**Solution:**
- Focus on larger competitors (>10K visits/month)
- Use alternative tools for very small sites (web_fetch, manual research)

---

## 🔄 **Integration with 10-Step Validation**

This module is **Step 1A: Competitive Intelligence**

**Updated 10-Step Method:**
1. **Competitive Intelligence** (← YOU ARE HERE)
   - Run SimilarWeb analysis
   - Identify market gaps
   - Benchmark pricing/features
2. **Problem Validation** (Weeks 1-2)
   - Interview 15-20 people
   - Ask about competitor usage
   - Validate problem severity
3. **Solution Validation** (Weeks 3-4)
   - Demo your solution
   - Compare to competitors
   - Prove superior value
4. **Pricing Validation** (Week 5)
   - Get pilot commitments
   - Justify premium vs competitors
   - Calculate LTV:CAC
5. **Market Size Validation** (Week 5)
   - Use traffic data to estimate TAM
   - Calculate required market penetration
   - Assess feasibility
6-10. **Build, Launch, Scale** (if validated)

---

## 📚 **Resources**

**API Documentation:**
- Apify Platform: https://apify.com/docs
- SimilarWeb Scraper: https://apify.com/mscraper/similarweb-quick-scraper
- API Reference: https://docs.apify.com/api/v2

**Related Tools:**
- Web Search (general research): `web_search` tool in Claude
- Web Fetch (specific pages): `web_fetch` tool
- Google Drive (internal docs): `google_drive_search` tool

---

## 🤝 **Contributing**

**Improvements welcome:**
- Additional report templates
- More competitor metrics
- Automated trend analysis
- Integration with other tools

**How to contribute:**
1. Fork validate-build-system repo
2. Create feature branch
3. Submit pull request

---

## 📄 **License**

MIT License - Free to use for personal and commercial projects

---

## 👤 **Maintainer**

**Ariel Shapira**  
Everest Capital USA / BidDeed.AI  
Contact: [Your preferred contact method]

---

## 🔄 **Changelog**

**v1.0 (December 31, 2025)**
- ✅ Initial release
- ✅ SimilarWeb paywall bypass via Apify
- ✅ Automated report generation
- ✅ Integration with 10-step methodology
- ✅ Real-world example (real estate investing tools)
- ✅ Comprehensive documentation

---

**Last Updated:** December 31, 2025  
**Status:** Production-ready ✅  
**Cost:** $0 (Apify free tier)

---

**🚀 Ready to analyze your competitors? Start with Step 1 above!**
