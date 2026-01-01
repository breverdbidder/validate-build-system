#!/usr/bin/env python3
"""
Generate executive summary from competitor analysis results

Usage:
    python3 generate_summary.py \
        --input results/analysis_20251231.json \
        --product-name "BidDeed.AI" \
        --product-focus "Foreclosure auction intelligence" \
        --target-users 5000 \
        --target-arpu 297 \
        --output results/EXEC_SUMMARY_20251231.md
"""

import json
import argparse
from datetime import datetime


def generate_summary(data, product_name, product_focus, target_users, target_arpu):
    """Generate markdown executive summary from competitor data"""
    
    competitors = data["competitors"]
    scraped_at = data["metadata"]["scraped_at"]
    
    # Calculate market totals
    total_visits = sum(
        c["traffic"]["current_visits"] or 0 
        for c in competitors
    )
    
    # Sort by traffic
    competitors_sorted = sorted(
        competitors,
        key=lambda x: x["traffic"]["current_visits"] or 0,
        reverse=True
    )
    
    # Generate markdown
    md = f"""# 📊 COMPETITIVE INTELLIGENCE REPORT
## {product_name} - Market Analysis via SimilarWeb

**Generated:** {datetime.now().strftime('%B %d, %Y, %I:%M %p EST')}  
**Data Source:** SimilarWeb (via Apify API - Paywall Bypassed ✅)  
**Competitors Analyzed:** {len(competitors)}  
**Total Market Traffic:** {total_visits:,} monthly visits  
**Cost:** $0 (Apify free tier)

---

## 🎯 **{product_name.upper()} POSITIONING**

**Product Focus:** {product_focus}  
**Target Users (Year 5):** {target_users:,}  
**Target ARPU:** ${target_arpu}/month  
**Target ARR (Year 5):** ${target_users * target_arpu * 12:,}

---

## 📊 **COMPETITOR TRAFFIC OVERVIEW**

"""
    
    # Add competitor table
    md += "| Rank | Platform | Monthly Visits | Market Share | Bounce Rate | Pages/Visit | Time on Site |\n"
    md += "|------|----------|---------------|--------------|-------------|-------------|-------------|\n"
    
    for i, comp in enumerate(competitors_sorted, 1):
        domain = comp["domain"]
        visits = comp["traffic"]["current_visits"]
        bounce = comp["engagement"]["bounce_rate"]
        pages = comp["engagement"]["pages_per_visit"]
        time_sec = comp["engagement"]["time_on_site_seconds"]
        
        visits_str = f"{visits:,}" if visits else "N/A"
        bounce_str = f"{bounce:.1f}%" if bounce else "N/A"
        pages_str = f"{pages:.2f}" if pages else "N/A"
        
        if time_sec:
            minutes = int(time_sec // 60)
            seconds = int(time_sec % 60)
            time_str = f"{minutes}m {seconds}s"
        else:
            time_str = "N/A"
        
        market_share = (visits / total_visits * 100) if visits and total_visits else 0
        
        md += f"| #{i} | **{domain}** | {visits_str} | {market_share:.1f}% | {bounce_str} | {pages_str} | {time_str} |\n"
    
    # Add detailed analysis for each competitor
    md += "\n---\n\n## 🔍 **DETAILED COMPETITOR ANALYSIS**\n\n"
    
    for i, comp in enumerate(competitors_sorted, 1):
        domain = comp["domain"]
        
        md += f"### {i}. {domain.upper()}\n\n"
        
        # Rankings
        global_rank = comp["rankings"]["global_rank"]
        country_rank = comp["rankings"]["country_rank"]
        country_code = comp["rankings"]["country_code"]
        category = comp["rankings"]["category"]
        category_rank = comp["rankings"]["category_rank"]
        
        md += "**Rankings:**\n"
        if global_rank:
            md += f"- 🌍 Global: #{global_rank:,}\n"
        if country_rank:
            md += f"- 🇺🇸 {country_code}: #{country_rank:,}\n"
        if category != "N/A":
            md += f"- 📂 Category: {category.replace('_', ' ').title()}\n"
        if category_rank:
            md += f"- 🏆 Category Rank: #{category_rank}\n"
        md += "\n"
        
        # Traffic trend
        monthly_visits = comp["traffic"]["monthly_visits"]
        if monthly_visits and len(monthly_visits) >= 2:
            sorted_months = sorted(monthly_visits.items(), reverse=True)[:3]
            md += "**Traffic Trend (Last 3 Months):**\n"
            for month, visits in sorted_months:
                md += f"- {month}: {visits:,}\n"
            md += "\n"
        
        # Traffic sources
        traffic_sources = comp["traffic_sources"]
        if traffic_sources:
            md += "**Traffic Sources:**\n"
            for source, pct in sorted(traffic_sources.items(), key=lambda x: x[1], reverse=True):
                if pct > 0.001:  # Only show >0.1%
                    md += f"- {source}: {pct*100:.2f}%\n"
            md += "\n"
        
        # Geographic distribution
        top_countries = comp["top_countries"]
        if top_countries:
            md += "**Geographic Distribution (Top 5):**\n"
            for country_data in top_countries:
                code = country_data.get('CountryCode', 'N/A')
                value = country_data.get('Value', 0) * 100
                md += f"- {code}: {value:.2f}%\n"
            md += "\n"
        
        # Description
        description = comp.get("description", "")
        if description:
            md += f"**Description:**  \n{description}\n\n"
        
        md += "---\n\n"
    
    # Add strategic insights
    required_annual_visitors = target_users / 0.15  # Assuming 15% conversion
    required_monthly_visits = required_annual_visitors / 12
    market_penetration = (required_monthly_visits / total_visits * 100) if total_visits else 0
    
    md += f"""## 🎯 **STRATEGIC INSIGHTS FOR {product_name.upper()}**

### Market Size Analysis

**Total Addressable Market (TAM):**
- Combined competitor traffic: {total_visits:,} monthly visits
- Estimated market revenue: (Calculate based on competitor ARPUs)

**{product_name} Target:**
- Year 5 users: {target_users:,}
- Year 5 ARR: ${target_users * target_arpu * 12:,}

### Traffic Requirements

**Assuming 15% annual conversion rate:**
```
Required annual visitors: {required_annual_visitors:,.0f}
Required monthly visits: {required_monthly_visits:,.0f}
Market penetration needed: {market_penetration:.2f}%
```

**Feasibility Assessment:**
- ✅ **ACHIEVABLE** if penetration <5%
- ⚠️ **AGGRESSIVE** if penetration 5-10%
- ❌ **UNREALISTIC** if penetration >10%

### Engagement Benchmarks

**Based on competitor analysis, target metrics for {product_name}:**

| Metric | Best in Class | Good | Target for {product_name} |
|--------|---------------|------|---------------------------|
| Bounce Rate | <40% | 40-50% | <45% |
| Pages per Visit | 8-10 | 5-7 | 5-7 |
| Time on Site | 5+ min | 3-5 min | 3-5 min |
| Direct Traffic | 70%+ | 60-70% | 60%+ by Year 3 |

### Competitive Positioning

**{product_name} Differentiation:**
- **Focus:** {product_focus}
- **Unique Value:** [Define your unique features here]
- **Target Niche:** [Define your specific customer segment]

**Feature Gap Analysis:**
- Table-stakes features ALL competitors have: [List here]
- Unique features NO competitors have: [List here]
- Missing features you MUST build: [List here]

---

## 📋 **VALIDATION PROTOCOL**

### Step 1A: Competitive Intelligence (✅ COMPLETE)

You've successfully bypassed SimilarWeb paywall and analyzed {len(competitors)} competitors.

### Next Steps: Problem Validation (Weeks 1-2)

**Interview Questions (15-20 interviews):**
1. "Do you currently use {', '.join([c['domain'] for c in competitors_sorted[:3]])}?"
2. "What do you like/dislike about those tools?"
3. "What's missing from those tools for {product_focus.lower()}?"
4. "Have you lost money due to [specific problem]?"
5. "How much would you pay monthly to prevent that loss?"

**Success Criteria:**
- ✅ 15+ confirm the problem exists
- ✅ 10+ willing to pay ${target_arpu}/month
- ✅ Average loss >10x annual subscription cost

### Pricing Strategy

**Competitor ARPU Estimates:**
"""
    
    # Add competitor pricing estimates
    for comp in competitors_sorted:
        domain = comp["domain"]
        visits = comp["traffic"]["current_visits"]
        # Rough ARPU estimation based on traffic
        if visits and visits > 50000:
            est_arpu = "$40-60/mo"
        elif visits and visits > 10000:
            est_arpu = "$20-40/mo"
        else:
            est_arpu = "$10-30/mo"
        
        md += f"- {domain}: Estimated {est_arpu}\n"
    
    md += f"""
**{product_name} Pricing:**
- Target ARPU: ${target_arpu}/month
- Premium vs competitors: {(target_arpu / 40):.1f}x average
- Justification needed: [Must prevent ${target_arpu * 10:,}+ in losses per year]

---

## 🔬 **DATA QUALITY NOTES**

**Data Source:** SimilarWeb (via Apify API)  
**Accuracy:** SimilarWeb estimates are typically ±20% accurate  
**Data Date:** {scraped_at[:10]}  
**Refresh Frequency:** Run monthly to track trends

**Limitations:**
- SimilarWeb requires minimum traffic thresholds (~1K visits/month)
- Small sites may show "N/A" for some metrics
- Engagement metrics are estimates, not exact

---

## 📁 **FILES GENERATED**

1. **Raw Data:** JSON file with complete SimilarWeb response
2. **This Report:** Markdown executive summary
3. **Next:** Use this data to refine validation interviews

---

**Generated by:** Validate-Build System  
**Competitive Intel Module:** v1.0  
**Report Date:** {datetime.now().strftime('%B %d, %Y')}

---

## 🚀 **IMMEDIATE NEXT STEPS**

1. ✅ **Review this report** thoroughly
2. ✅ **Try competitor products** (sign up for free trials)
3. ✅ **Update interview script** with competitor context
4. ✅ **Refine pricing strategy** based on market data
5. ✅ **Plan MVP features** (table-stakes + differentiation)

**Then proceed to Problem Validation (Step 1 of 10-Step Method).**

---

**🔓 Paywall Bypass Method:**
- Tool: Apify API (mscraper~similarweb-quick-scraper)
- Cost: $0 (free tier)
- Setup time: 5 minutes
- Data quality: Production-grade

**Repeat this analysis monthly to track competitor growth trends.**
"""
    
    return md


def main():
    parser = argparse.ArgumentParser(
        description="Generate executive summary from competitor analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--input', required=True, help='Input JSON file from analyze_competitors.py')
    parser.add_argument('--output', required=True, help='Output markdown file path')
    parser.add_argument('--product-name', required=True, help='Your product name (e.g., "BidDeed.AI")')
    parser.add_argument('--product-focus', required=True, help='Your product focus/niche (e.g., "Foreclosure auction intelligence")')
    parser.add_argument('--target-users', type=int, required=True, help='Target user count for Year 5 (e.g., 5000)')
    parser.add_argument('--target-arpu', type=int, required=True, help='Target ARPU in dollars per month (e.g., 297)')
    
    args = parser.parse_args()
    
    # Load data
    try:
        with open(args.input, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Input file not found: {args.input}")
        print(f"Run analyze_competitors.py first to generate the data file.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON in {args.input}")
        sys.exit(1)
    
    # Generate summary
    summary = generate_summary(
        data,
        args.product_name,
        args.product_focus,
        args.target_users,
        args.target_arpu
    )
    
    # Save
    with open(args.output, 'w') as f:
        f.write(summary)
    
    print(f"\n✅ Executive summary generated: {args.output}")
    print(f"\n📊 Summary:")
    print(f"   - Product: {args.product_name}")
    print(f"   - Focus: {args.product_focus}")
    print(f"   - Target Users: {args.target_users:,}")
    print(f"   - Target ARPU: ${args.target_arpu}/mo")
    print(f"   - Target ARR (Y5): ${args.target_users * args.target_arpu * 12:,}")
    print(f"\n🚀 Next: Review {args.output} and proceed with validation interviews!")


if __name__ == "__main__":
    main()
