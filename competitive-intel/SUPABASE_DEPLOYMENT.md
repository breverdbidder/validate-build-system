# 🗄️ Supabase Deployment Guide
## Competitive Intelligence Data Persistence

This guide explains how to deploy the Supabase schema for persistent competitor tracking.

---

## 📊 **Why Use Supabase?**

**Without Supabase:**
- Data stored in local JSON files
- No trend analysis over time
- Manual monthly comparisons
- No automated alerts

**With Supabase:**
- ✅ Time-series competitor tracking
- ✅ Automated trend analysis (MoM growth)
- ✅ Market share calculations
- ✅ SQL queries for custom insights
- ✅ API access for dashboards

---

## 🚀 **Quick Setup (5 Minutes)**

### Step 1: Get Supabase Credentials

You already have a Supabase project:
- **Project:** `mocerqjnksmhcjzxrewo`
- **URL:** `https://mocerqjnksmhcjzxrewo.supabase.co`

**Get your credentials:**
1. Go to: https://supabase.com/dashboard/project/mocerqjnksmhcjzxrewo/settings/api
2. Copy **"service_role" key** (the long one with warning ⚠️)
3. Keep it safe (this is your admin key)

### Step 2: Run Schema Migration

**Option A: Via Supabase Dashboard (Easiest)**

1. Go to: https://supabase.com/dashboard/project/mocerqjnksmhcjzxrewo/editor
2. Click "SQL Editor"
3. Click "New Query"
4. Copy contents of `supabase_schema.sql`
5. Paste and click "Run"
6. ✅ Done! Tables created.

**Option B: Via Command Line (Recommended)**

```bash
# Set credentials
export SUPABASE_URL="https://mocerqjnksmhcjzxrewo.supabase.co"
export SUPABASE_SERVICE_KEY="your_service_role_key_here"

# Run migration
psql "postgresql://postgres:your_db_password@db.mocerqjnksmhcjzxrewo.supabase.co:5432/postgres" \
  < supabase_schema.sql
```

**Option C: Via GitHub Actions (Automated)**

```bash
# Add secrets to GitHub repo
gh secret set SUPABASE_URL --body "https://mocerqjnksmhcjzxrewo.supabase.co"
gh secret set SUPABASE_SERVICE_KEY --body "your_service_role_key_here"

# GitHub Action will auto-deploy on next push
```

### Step 3: Update Scripts to Save to Supabase

**The scripts already support Supabase!** Just set environment variables:

```bash
# Add to .env file
echo "SUPABASE_URL=https://mocerqjnksmhcjzxrewo.supabase.co" >> .env
echo "SUPABASE_SERVICE_KEY=your_service_role_key_here" >> .env

# Scripts will automatically detect and save to Supabase
```

---

## 📊 **What Gets Stored**

### Table 1: `competitor_snapshots`
**Time-series competitor data**

Every time you run `analyze_competitors.py`, it saves:
- Monthly traffic counts
- Engagement metrics (bounce rate, pages/visit, time on site)
- Rankings (global, country, category)
- Traffic sources (direct, search, social, etc.)
- Raw SimilarWeb response (JSONB)

**Example Row:**
```json
{
  "domain": "dealcheck.io",
  "monthly_visits": 48079,
  "visits_month": "2025-11",
  "bounce_rate": 38.50,
  "pages_per_visit": 9.74,
  "time_on_site_seconds": 339,
  "global_rank": 364875,
  "country_rank": 84680,
  "direct_traffic": 72.93,
  "search_traffic": 22.14,
  "scraped_at": "2025-12-31T23:45:00Z"
}
```

### Table 2: `competitive_analyses`
**Analysis metadata and reports**

Tracks each competitive analysis run:
- Product name and focus
- Target users/ARPU/ARR
- Total market size
- Number of competitors
- Validation score (0-100)
- Key findings and recommendations

**Example Row:**
```json
{
  "analysis_name": "Real Estate Tools Q4 2025",
  "product_name": "BidDeed.AI",
  "product_focus": "Foreclosure auction intelligence",
  "target_users": 5000,
  "target_arpu": 297,
  "target_arr": 17820000,
  "total_market_visits": 187555,
  "num_competitors": 4,
  "required_monthly_visits": 2778,
  "market_penetration_pct": 1.48,
  "validation_score": 82,
  "key_findings": ["PropertyOnion is market leader", "DealCheck declining -22%"],
  "recommendations": ["Focus on foreclosure niche", "Premium pricing justified"]
}
```

### View 1: `competitor_trends`
**Monthly aggregated metrics**

```sql
SELECT * FROM competitor_trends 
WHERE domain = 'dealcheck.io' 
ORDER BY month DESC 
LIMIT 6;
```

**Output:**
```
domain         | month     | avg_visits | avg_bounce_rate | avg_pages_per_visit
---------------|-----------|------------|-----------------|-------------------
dealcheck.io   | 2025-11   | 48079      | 38.50           | 9.74
dealcheck.io   | 2025-10   | 61921      | 39.20           | 9.65
dealcheck.io   | 2025-09   | 62466      | 38.80           | 9.81
```

**Insight:** Declining traffic (-22% Nov vs Oct)

### View 2: `market_share`
**Relative market positioning**

```sql
SELECT * FROM market_share 
WHERE visits_month = '2025-11' 
ORDER BY market_share_pct DESC;
```

**Output:**
```
domain              | monthly_visits | total_market | market_share_pct
--------------------|----------------|--------------|------------------
propertyonion.com   | 85234          | 187555       | 45.44
rehabvaluator.com   | 50432          | 187555       | 26.88
dealcheck.io        | 48079          | 187555       | 25.63
zilculator.com      | 3810           | 187555       | 2.03
```

**Insight:** PropertyOnion is market leader (45% share)

---

## 🔍 **Useful SQL Queries**

### 1. Track Competitor Growth

```sql
SELECT 
    domain,
    visits_month,
    monthly_visits,
    LAG(monthly_visits) OVER (PARTITION BY domain ORDER BY visits_month) as prev_month,
    ROUND(
        ((monthly_visits - LAG(monthly_visits) OVER (PARTITION BY domain ORDER BY visits_month))::NUMERIC 
        / NULLIF(LAG(monthly_visits) OVER (PARTITION BY domain ORDER BY visits_month), 0)) * 100,
        2
    ) as mom_growth_pct
FROM competitor_snapshots
WHERE visits_month >= '2025-09'
ORDER BY domain, visits_month DESC;
```

### 2. Compare Engagement Quality

```sql
SELECT 
    domain,
    AVG(bounce_rate) as avg_bounce,
    AVG(pages_per_visit) as avg_pages,
    AVG(time_on_site_seconds) as avg_time,
    CASE 
        WHEN AVG(bounce_rate) < 40 AND AVG(pages_per_visit) > 8 THEN 'Excellent'
        WHEN AVG(bounce_rate) < 50 AND AVG(pages_per_visit) > 5 THEN 'Good'
        ELSE 'Poor'
    END as engagement_quality
FROM competitor_snapshots
WHERE visits_month = '2025-11'
GROUP BY domain
ORDER BY engagement_quality DESC, avg_time DESC;
```

### 3. Alert on Traffic Drops

```sql
WITH monthly_changes AS (
    SELECT 
        domain,
        visits_month,
        monthly_visits,
        LAG(monthly_visits) OVER (PARTITION BY domain ORDER BY visits_month) as prev_visits,
        ((monthly_visits - LAG(monthly_visits) OVER (PARTITION BY domain ORDER BY visits_month))::NUMERIC 
        / NULLIF(LAG(monthly_visits) OVER (PARTITION BY domain ORDER BY visits_month), 0)) * 100 as change_pct
    FROM competitor_snapshots
)
SELECT *
FROM monthly_changes
WHERE change_pct < -15  -- Alert if traffic drops >15%
ORDER BY change_pct ASC;
```

**Output:**
```
domain        | visits_month | monthly_visits | prev_visits | change_pct
--------------|--------------|----------------|-------------|------------
dealcheck.io  | 2025-11      | 48079          | 61921       | -22.34
```

**Alert:** DealCheck traffic dropped 22.34% in November!

---

## 🔄 **Automated Monthly Tracking**

### Option 1: GitHub Actions (Recommended)

Create `.github/workflows/monthly_competitor_tracking.yml`:

```yaml
name: Monthly Competitor Tracking

on:
  schedule:
    - cron: '0 0 1 * *'  # First day of every month
  workflow_dispatch:  # Manual trigger

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd competitive-intel
          pip install -r requirements.txt
      
      - name: Run analysis
        env:
          APIFY_API_TOKEN: ${{ secrets.APIFY_API_TOKEN }}
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_SERVICE_KEY: ${{ secrets.SUPABASE_SERVICE_KEY }}
        run: |
          cd competitive-intel
          python3 scripts/analyze_competitors.py \
            --domains "propertyonion.com,rehabvaluator.com,dealcheck.io,zilculator.com" \
            --output results/monthly_$(date +%Y%m).json \
            --save-to-supabase
      
      - name: Generate report
        run: |
          cd competitive-intel
          python3 scripts/generate_summary.py \
            --input results/monthly_$(date +%Y%m).json \
            --product-name "BidDeed.AI" \
            --product-focus "Foreclosure auction intelligence" \
            --target-users 5000 \
            --target-arpu 297 \
            --output results/MONTHLY_REPORT_$(date +%Y%m).md
      
      - name: Commit results
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add competitive-intel/results/
          git commit -m "Automated monthly competitor analysis $(date +%Y-%m)" || echo "No changes"
          git push || echo "Nothing to push"
```

**Setup:**
```bash
gh secret set SUPABASE_URL --body "https://mocerqjnksmhcjzxrewo.supabase.co"
gh secret set SUPABASE_SERVICE_KEY --body "your_service_role_key_here"
```

### Option 2: Cron Job (Local)

```bash
# Add to crontab
crontab -e

# Add this line (runs first day of every month at midnight)
0 0 1 * * cd /path/to/validate-build-system/competitive-intel && \
  /usr/bin/python3 scripts/analyze_competitors.py \
  --domains "comp1.com,comp2.com" \
  --output results/monthly_$(date +\%Y\%m).json \
  --save-to-supabase
```

---

## 📈 **Dashboard Integration (Future)**

Once data is in Supabase, you can:

1. **Build a Retool Dashboard**
   - Connect to Supabase
   - Show competitor trends over time
   - Alert on traffic drops >15%

2. **Use Supabase Charts**
   - Built-in visualization
   - No code required
   - Auto-refresh

3. **Export to Sheets**
   - Query Supabase via API
   - Auto-populate Google Sheets
   - Share with team

---

## 🐛 **Troubleshooting**

### Error: "relation already exists"
**Cause:** Schema already deployed  
**Solution:** Safe to ignore, or drop tables first:

```sql
DROP TABLE IF EXISTS competitor_snapshots CASCADE;
DROP TABLE IF EXISTS competitive_analyses CASCADE;
DROP VIEW IF EXISTS competitor_trends;
DROP VIEW IF EXISTS market_share;
```

### Error: "permission denied"
**Cause:** Using anon key instead of service_role key  
**Solution:** Get service_role key from Settings > API

### Data not saving to Supabase
**Cause:** Environment variables not set  
**Solution:**
```bash
export SUPABASE_URL="https://mocerqjnksmhcjzxrewo.supabase.co"
export SUPABASE_SERVICE_KEY="your_key_here"
```

---

## 📋 **Deployment Checklist**

- [ ] Get Supabase service_role key
- [ ] Run `supabase_schema.sql` in SQL Editor
- [ ] Verify tables created (competitor_snapshots, competitive_analyses)
- [ ] Set SUPABASE_URL and SUPABASE_SERVICE_KEY env vars
- [ ] Run analyze_competitors.py with --save-to-supabase flag
- [ ] Check Supabase dashboard for data
- [ ] Set up monthly GitHub Action (optional)
- [ ] Create trend analysis queries (optional)

---

## 🎯 **Next Steps**

1. **Deploy schema** (5 minutes)
2. **Run first analysis** with Supabase enabled
3. **Verify data** in Supabase dashboard
4. **Set up monthly automation** (GitHub Actions)
5. **Build dashboard** (Retool/Supabase Charts)

---

**Need help?** Check the main competitive-intel README or raise an issue on GitHub.
