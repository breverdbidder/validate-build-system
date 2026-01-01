# 🎯 Validation Automation System

**Automated infrastructure for the VALIDATE→BUILD methodology**

Deploy landing pages, track interviews, calculate validation scores - all automated.

## 🚀 Quick Start

### Deploy Landing Pages (1 command)

```bash
# Deploy both landing pages to Cloudflare Pages
./deploy/deploy_all.sh
```

**Live URLs:**
- Zoning Analyst: `https://validate-zoning.pages.dev`
- Lien Discovery: `https://validate-lien.pages.dev`
- Validation Dashboard: `https://validate-dashboard.pages.dev`

### Track Interviews

```bash
# Add interview to tracker
python3 validation-tracker/add_interview.py \
  --tool "Zoning Analyst" \
  --contact "John Smith, ABC Development" \
  --pain_score 9 \
  --would_pay "Yes" \
  --amount 297
```

### Calculate Validation Score

```bash
# Get current validation score
python3 validation-tracker/calculate_score.py --tool "Zoning Analyst"

# Output:
# Validation Score: 68/100 (68%)
# Status: ✅ GREEN - PROCEED TO BUILD
```

---

## 📊 System Overview

### Architecture

```
┌─────────────────────────────────────────────┐
│         Landing Pages (Cloudflare)          │
│  - Zoning Analyst                           │
│  - Lien Discovery                           │
│  - Conversion-optimized                     │
└─────────────────┬───────────────────────────┘
                  │
                  │ Analytics Events
                  ▼
┌─────────────────────────────────────────────┐
│         Supabase Database                   │
│  - visitors (landing page traffic)          │
│  - interviews (user validation)             │
│  - validation_scores (calculated)           │
└─────────────────┬───────────────────────────┘
                  │
                  │ Queries
                  ▼
┌─────────────────────────────────────────────┐
│      Validation Dashboard (React)           │
│  - Real-time metrics                        │
│  - Interview tracker                        │
│  - Decision matrix                          │
└─────────────────────────────────────────────┘
```

---

## 🗂️ Repository Structure

```
validate-build-system/
├── landing-pages/
│   ├── zoning-analyst/
│   │   └── index.html          # Zoning Analyst landing page
│   ├── lien-discovery/
│   │   └── index.html          # Lien Discovery landing page
│   └── shared/
│       ├── styles.css          # Shared CSS
│       └── analytics.js        # Analytics tracking
├── validation-tracker/
│   ├── add_interview.py        # Add interview to database
│   ├── calculate_score.py      # Calculate validation score
│   ├── interview_tracker.py    # Interview management
│   └── dashboard.html          # Validation dashboard
├── automation/
│   ├── email-templates/
│   │   ├── linkedin_outreach.txt
│   │   ├── interview_invite.txt
│   │   └── followup.txt
│   └── scripts/
│       ├── schedule_interviews.py
│       └── send_emails.py
├── deploy/
│   ├── supabase_schema.sql     # Database schema
│   ├── cloudflare_deploy.yml   # CI/CD config
│   └── deploy_all.sh           # One-click deployment
└── docs/
    ├── METHODOLOGY.md          # VALIDATE→BUILD explained
    ├── DECISION_MATRIX.md      # Go/No-Go criteria
    └── INTERVIEW_GUIDE.md      # Mom Test questions
```

---

## 🎯 Features

### 1. Landing Pages (Conversion-Optimized)

**Zoning Analyst Pro™:**
- Headline: "Know the Optimal Development Strategy in 15 Minutes, Not 15 Days"
- 3-tier CTA strategy (Trial, Demo, Guide)
- Wizard of Oz demo (Bliss sample report)
- Social proof placeholders
- Analytics tracking

**Lien Discovery Agent™:**
- Headline: "Discover All Liens in 10 Minutes, Prevent $100K+ Title Defects"
- 3-tier CTA strategy
- HOA foreclosure detection demo
- Title company testimonials
- Real-time analytics

### 2. Interview Tracking (Supabase)

**Database Schema:**
- `visitors` - Landing page traffic, CTA clicks
- `interviews` - User interview data (Mom Test responses)
- `validation_scores` - Calculated scores per tool

**Features:**
- Real-time interview logging
- Pain score tracking (1-10)
- Willingness-to-pay capture
- Automated score calculation

### 3. Validation Scorecard Calculator

**Metrics Tracked:**
- Landing page visits
- CTA conversion rate
- Interview count
- Would-pay percentage
- Qualitative signals
- Warning signals

**Scoring:**
- GREEN (60+/100): Build immediately
- YELLOW (40-59/100): Pivot and re-validate
- RED (<40/100): Kill project

### 4. Email Automation

**Templates Included:**
- LinkedIn outreach (cold)
- Interview invitation
- Follow-up sequences
- Thank you + gift card delivery

**Integration:** Ready for SendGrid, Mailgun, or manual use

---

## 📈 Usage Workflow

### Week 1: Deploy Landing Pages

```bash
# 1. Deploy to Cloudflare Pages
./deploy/deploy_all.sh

# 2. Verify deployment
curl -I https://validate-zoning.pages.dev
curl -I https://validate-lien.pages.dev

# 3. Set up analytics
# Edit landing-pages/shared/analytics.js
# Add your Google Analytics ID
```

### Week 2-3: Drive Traffic

```bash
# 1. Run Facebook Ads (manual - see docs/FACEBOOK_ADS.md)
# 2. LinkedIn outreach
python3 automation/scripts/send_emails.py \
  --template linkedin_outreach \
  --list contacts.csv

# 3. Monitor traffic
python3 validation-tracker/dashboard.py --live
```

### Week 3-5: Conduct Interviews

```bash
# 1. Schedule interviews via Calendly (manual)

# 2. Conduct interview (use docs/INTERVIEW_GUIDE.md)

# 3. Log interview
python3 validation-tracker/add_interview.py \
  --tool "Zoning Analyst" \
  --contact "Jane Doe, DEF Developers" \
  --pain_score 8 \
  --would_pay "Yes" \
  --amount 297 \
  --urgency "High" \
  --notes "Has Bliss-like project starting in March"

# 4. Repeat 15-20 times per tool
```

### Week 5: Calculate Validation Score

```bash
# Get final score
python3 validation-tracker/calculate_score.py --tool "Zoning Analyst"

# Output example:
# ========================================
# VALIDATION SCORECARD: Zoning Analyst Pro
# ========================================
# 
# QUANTITATIVE METRICS:
# - Landing page visits: 287 (57/100)
# - CTA conversion: 8.4% (84/100)
# - User interviews: 18 (100/100)
# - Would pay %: 44% (73/100)
# Subtotal: 314/400
# 
# QUALITATIVE SIGNALS:
# - Feature requests: 12
# - Urgency count: 9
# - Referrals: 3
# Subtotal: 24/100
# 
# TOTAL SCORE: 338/500 (68%)
# STATUS: ✅ GREEN - PROCEED TO BUILD
# 
# DECISION: Build MVP immediately
# ESTIMATED TIME TO $3K/MONTH: 3-4 months
```

---

## 🔧 Setup & Configuration

### Prerequisites

- Python 3.11+
- Node.js 18+ (for Cloudflare Pages)
- Git
- Supabase account (free tier)
- Cloudflare account (free tier)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/breverdbidder/validate-build-system.git
cd validate-build-system

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Set up Supabase
# - Create project at supabase.com
# - Run deploy/supabase_schema.sql
# - Copy .env.example to .env
# - Add SUPABASE_URL and SUPABASE_KEY

# 4. Deploy to Cloudflare
npm install -g wrangler
wrangler login
./deploy/deploy_all.sh
```

### Environment Variables

```bash
# .env file
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
CLOUDFLARE_ACCOUNT_ID=your-account-id
```

---

## 📊 Validation Criteria

### Quantitative Thresholds (ALL required for GREEN)

| Metric | Zoning Analyst | Lien Discovery |
|--------|---------------|----------------|
| Landing page visits | 200+ | 500+ |
| CTA conversion | 8%+ | 5%+ |
| User interviews | 15+ | 15+ |
| Would pay % | 30%+ | 30%+ |
| **Validation score** | **60+/100** | **60+/100** |

### Qualitative Signals (need 3+)

- [ ] Unprompted feature requests
- [ ] "When can I buy?" urgency
- [ ] Referrals to other potential customers
- [ ] Emotional intensity about problem

### Warning Signals (any = concern)

- [ ] "Nice to have" language
- [ ] No urgency to solve problem
- [ ] Price sensitivity ("too expensive")
- [ ] Can't clearly articulate problem

---

## 🚀 Deployment

### Cloudflare Pages Deployment

```bash
# Automatic deployment (one command)
./deploy/deploy_all.sh

# Manual deployment
cd landing-pages/zoning-analyst
npx wrangler pages deploy . --project-name=validate-zoning

cd ../lien-discovery
npx wrangler pages deploy . --project-name=validate-lien
```

### Supabase Setup

```bash
# 1. Create Supabase project
# 2. Run schema
psql -h db.your-project.supabase.co -U postgres -d postgres -f deploy/supabase_schema.sql

# 3. Verify tables
python3 -c "
from supabase import create_client
import os
supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY'))
print(supabase.table('interviews').select('*').execute())
"
```

---

## 📚 Documentation

- **[METHODOLOGY.md](docs/METHODOLOGY.md)** - Complete VALIDATE→BUILD 10-step process
- **[DECISION_MATRIX.md](docs/DECISION_MATRIX.md)** - Go/No-Go decision criteria
- **[INTERVIEW_GUIDE.md](docs/INTERVIEW_GUIDE.md)** - Mom Test interview questions

---

## 🤝 Contributing

This is an internal tool for Everest Capital / BidDeed.AI validation workflows.

**Improvements welcome:**
- Better landing page designs
- Additional email templates
- Enhanced scorecard algorithms
- Integrations (Calendly, SendGrid, etc.)

---

## 📄 License

Proprietary - Everest Capital USA / BidDeed.AI

---

## 🎯 What's Next?

After validation completes:

### If GREEN (60+/100):
```bash
# Create MVP repository
cd /path/to/projects
git clone https://github.com/breverdbidder/[tool-name]-mvp.git

# Begin 6-week BUILD phase
# Deploy beta with 10-20 users
# Target: $3K+/month net income
```

### If YELLOW (40-59/100):
```bash
# Pivot and re-validate
# Adjust pricing or target market
# Run validation again with new assumptions
```

### If RED (<40/100):
```bash
# Kill project immediately
# Move to next tool validation
# Apply learnings to avoid same mistakes
```

---

**Built with ❤️ for autonomous validation at scale**

**Questions?** Review docs/ or run validation-tracker/dashboard.py
