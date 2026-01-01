# 🔬 Validate-Build System
## The Evidence-Based Product Development Framework

**Stop building products nobody wants.** Validate first, build second.

---

## 🎯 **What Is This?**

A systematic, data-driven framework for validating product ideas BEFORE writing code. Inspired by The Mom Test, Lean Startup, and real-world failures.

**The Problem:**
- 90% of startups fail
- #1 reason: No market need
- Root cause: Building before validating

**The Solution:**
- Spend $1,440 on validation (5 weeks)
- Save $19,800 on failed MVPs
- Kill bad ideas BEFORE wasting months

---

## 📊 **The 10-Step Methodology**

### **PHASE 1: VALIDATE (Weeks 1-5, $1,440)**

#### **Step 1A: Competitive Intelligence** 🆕
**Time:** 2-4 hours  
**Cost:** $0  
**Tools:** `competitive-intel/` module

**What you do:**
```bash
cd competitive-intel
python3 scripts/analyze_competitors.py \
  --domains "competitor1.com,competitor2.com,competitor3.com" \
  --output results/analysis_$(date +%Y%m%d).json

python3 scripts/generate_summary.py \
  --input results/analysis_*.json \
  --product-name "Your Product" \
  --product-focus "Your niche" \
  --target-users 5000 \
  --target-arpu 297 \
  --output results/EXEC_SUMMARY.md
```

**What you learn:**
- Market size (total addressable market)
- Competitor traffic & engagement
- Pricing benchmarks
- Feature gaps
- Growth trends

**Success criteria:**
- ✅ 3+ competitors analyzed
- ✅ Total market >100K visits/month
- ✅ Your target <5% market penetration
- ✅ Feature gaps identified

**See:** `competitive-intel/README.md` for full documentation

---

#### **Step 1: Problem Validation**
**Time:** 2 weeks  
**Cost:** $720 ($50/interview × 15 interviews - Wynter, UserInterviews)  
**Goal:** Confirm people have the problem

**What you do:**
- Interview 15-20 people in target market
- Ask about their current solutions (from Step 1A)
- Ask about pain points, not features
- Validate problem severity ($50K+ losses)

**Questions to ask:**
- "Walk me through your current process for [task]"
- "What tools do you currently use?" (mention competitors from Step 1A)
- "What's the biggest problem with [current solution]?"
- "Have you lost money due to [specific problem]?"
- "How much did you lose?" (target: $50K+)

**Success criteria:**
- ✅ 15+ people confirm problem exists
- ✅ 10+ currently pay for solutions (validates willingness to pay)
- ✅ Problem costs 10x+ annual subscription value

**Red flags:**
- ❌ People say "interesting idea" but can't cite specific pain
- ❌ No one currently pays for solutions
- ❌ Problem is "nice to have" not "must have"

---

#### **Step 2: Solution Validation**
**Time:** 2 weeks  
**Cost:** $360 ($60/demo × 6 mockups - Figma/Balsamiq)  
**Goal:** Confirm your solution solves the problem

**What you do:**
- Create mockups/prototypes (NOT code)
- Demo to 10 people from problem interviews
- Compare your solution to competitors (from Step 1A)
- Measure time-to-value (<10 min target)

**What to demo:**
- Key workflow (BID/REVIEW/SKIP in <10 seconds)
- Unique features competitors lack
- Value proposition (prevent $100K+ losses)

**Success criteria:**
- ✅ 8+ say "This solves my problem better than [competitor]"
- ✅ 8+ say "This would save me 10+ hours"
- ✅ Time-to-first-value <10 minutes (confirmed)

**Red flags:**
- ❌ People prefer current solutions
- ❌ "I'd need to see it working first"
- ❌ Features don't map to problems

---

#### **Step 3: Pricing Validation**
**Time:** 1 week  
**Cost:** $360 ($60/interview × 6 pricing calls)  
**Goal:** Confirm willingness to pay

**What you do:**
- Present pricing tiers
- Use competitor pricing as anchors (from Step 1A)
- Ask for pilot commitments
- Get LOIs or pre-orders

**Pricing framework:**
```
Value-based pricing:
- Competitor ARPU: $6-60/mo (from Step 1A)
- Your ARPU: $297-997/mo (premium)
- Justification: Prevent $100K+ loss = 100-336 months ROI
```

**Success criteria:**
- ✅ 5+ pilot commitments @ $297/mo
- ✅ 3+ pilot commitments @ $997/mo
- ✅ $10K+ in LOIs/deposits

**Red flags:**
- ❌ "Too expensive"
- ❌ "I'll wait until it's cheaper"
- ❌ No one commits with money

---

### **PHASE 2: BUILD (Months 1-6, $19,800)**

#### **Step 4: MVP Development**
- Only if Steps 1-3 score 60+/100
- Build minimum features to validate
- Launch to pilot users
- Iterate based on feedback

#### **Step 5: Beta Launch**
- Onboard pilot users
- Monitor engagement metrics
- Fix critical bugs
- Prepare for public launch

#### **Step 6-10: Scale**
- Public launch
- Marketing automation
- Team expansion
- Product-market fit optimization

---

## 🎯 **Validation Scorecard**

**Score each category, total out of 100:**

| Category | Points | Criteria |
|----------|--------|----------|
| **Problem (30 pts)** | 20 | 15+ interviews confirm $50K+ losses |
| | 10 | 10+ say "I'd pay $297/mo to avoid this" |
| **Solution (20 pts)** | 10 | Demo shows value in <10 min |
| | 10 | 80%+ say "saves 10+ hours" |
| **Pricing (30 pts)** | 15 | 5+ pilot commitments @ $297/mo |
| | 15 | 3+ pilot commitments @ $997/mo |
| **Market (20 pts)** | 10 | 200+ local investors identified |
| | 10 | 10K+ state/national TAM |

**Decision Matrix:**
- **80-100:** 🟢 BUILD IMMEDIATELY (high confidence)
- **60-79:** 🟡 BUILD WITH CAUTION (pivot pricing or features)
- **40-59:** 🟠 MAJOR PIVOTS NEEDED (different solution or market)
- **<40:** 🔴 KILL IDEA (save $19,800 on failed MVP)

---

## 📁 **Repository Structure**

```
validate-build-system/
├── README.md                          # This file
├── competitive-intel/                 # 🆕 Step 1A: Competitive Intelligence
│   ├── README.md                      # Full documentation
│   ├── requirements.txt               # Python dependencies
│   ├── scripts/
│   │   ├── analyze_competitors.py     # SimilarWeb scraper
│   │   └── generate_summary.py        # Report generator
│   ├── templates/                     # Report templates
│   └── results/                       # Generated reports (.gitignore)
├── validation-tracker/                # Scorecard & interview tracking
│   ├── scorecard.json                 # Live validation scores
│   └── interviews/                    # Interview notes
├── landing-pages/                     # Marketing site templates
│   ├── problem-validation/            # "We're solving X" page
│   ├── solution-validation/           # "Here's how" demo page
│   └── pricing-validation/            # "Join pilot" CTA page
└── deploy/                            # Cloudflare Pages configs
```

---

## 🚀 **Quick Start**

### Prerequisites
```bash
# Install dependencies
pip install -r competitive-intel/requirements.txt

# Set API credentials
echo "APIFY_API_TOKEN=your_token_here" >> .env
```

### Run Competitive Analysis (Step 1A)
```bash
cd competitive-intel

# Analyze competitors
python3 scripts/analyze_competitors.py \
  --domains "competitor1.com,competitor2.com" \
  --output results/analysis_$(date +%Y%m%d).json

# Generate report
python3 scripts/generate_summary.py \
  --input results/analysis_*.json \
  --product-name "Your Product" \
  --product-focus "Your niche" \
  --target-users 5000 \
  --target-arpu 297 \
  --output results/EXEC_SUMMARY.md

# Review results
cat results/EXEC_SUMMARY.md
```

**Time:** 30 minutes  
**Cost:** $0

### Proceed to Problem Validation (Step 1)
- Create interview script (use competitor insights)
- Schedule 15 interviews
- Track in `validation-tracker/`

---

## 💡 **Real-World Example: BidDeed.AI**

**Product:** Foreclosure auction intelligence  
**Market:** Real estate investors

### Step 1A Results (Competitive Intel)
```bash
python3 scripts/analyze_competitors.py \
  --domains "propertyonion.com,rehabvaluator.com,dealcheck.io,zilculator.com" \
  --output results/foreclosure_market.json
```

**Findings:**
- Total market: 187K visits/month
- PropertyOnion: 85K visits (leader, +18.9% growth)
- RehabValuator: 50K visits (+16.6% growth)
- DealCheck: 48K visits (declining -22.3%)
- Zilculator: 3.8K visits (tiny but growing)

**Strategic insight:** Market is fragmenting. Specialized tools (RehabValuator) outperforming generalists (DealCheck). Blue ocean opportunity in foreclosure niche.

### Steps 1-3 Results
- ✅ Problem: 18/20 interviews confirmed $50K+ lien losses
- ✅ Solution: 9/10 demos, avg 8min time-to-value
- ✅ Pricing: 7 pilot commitments ($297-997/mo)
- **Total Score: 82/100** → 🟢 **BUILD**

### Month 1-6: MVP
- Lien discovery automation
- BID/REVIEW/SKIP recommendations  
- ML purchase probability
- White-labeled PDF reports

**Outcome:** Launched to 50 pilot users, $14,850 MRR by Month 6

---

## 🎓 **Methodology Principles**

### 1. Evidence Over Opinions
- Don't ask "Would you buy this?"
- Ask "What did you pay last month for [solution]?"
- Track actual behavior, not stated preferences

### 2. Ruthless Prioritization
- Validate before building
- Kill ideas fast (save time & money)
- 80/20 rule: 20% of features = 80% of value

### 3. Competitive Context
- 🆕 Know your market BEFORE interviewing
- Use competitor data to ask better questions
- Benchmark pricing/features against reality
- Identify true differentiation

### 4. Quantified Risk
- $1,440 validation investment
- $19,800 MVP cost (if validated)
- 87% savings if idea fails validation
- 13x ROI if idea succeeds

---

## 📚 **Resources**

### Books
- The Mom Test (Rob Fitzpatrick)
- Lean Startup (Eric Ries)
- Zero to One (Peter Thiel)

### Tools
- **Competitive Intel:** Apify SimilarWeb scraper (this repo)
- **Interviews:** Wynter, UserInterviews, Calendly
- **Mockups:** Figma, Balsamiq
- **Analytics:** Google Analytics, Mixpanel
- **Landing Pages:** Cloudflare Pages (included)

### External APIs
- Apify (SimilarWeb data): https://apify.com
- RentCast (comps): https://rentcast.io
- Google Maps (local search): https://developers.google.com/maps

---

## 🤝 **Contributing**

Contributions welcome! Areas of interest:
- Additional validation templates
- More competitor analysis tools
- Interview question libraries
- Automated scorecard tracking
- Integration with other validation tools

---

## 📄 **License**

MIT License - Free for personal and commercial use

---

## 👤 **Maintainer**

**Ariel Shapira**  
Everest Capital USA / BidDeed.AI  
Validate-Build Methodology Creator

---

## 🔄 **Changelog**

### v2.0 (December 31, 2025) 🆕
- ✅ **Added Step 1A: Competitive Intelligence**
- ✅ SimilarWeb paywall bypass via Apify API
- ✅ Automated competitor traffic analysis
- ✅ Executive summary report generation
- ✅ Real-world example (real estate tools)
- ✅ Updated 10-step methodology
- ✅ Cost: $0 (Apify free tier)

### v1.0 (December 2025)
- ✅ Initial 10-step framework
- ✅ Validation scorecard
- ✅ Landing page templates
- ✅ Interview tracking

---

## 🎯 **Next Steps**

1. ✅ **Run competitive analysis** (Step 1A) - 30 minutes
2. ✅ **Schedule problem interviews** (Step 1) - 2 weeks
3. ✅ **Create solution mockups** (Step 2) - 2 weeks
4. ✅ **Get pilot commitments** (Step 3) - 1 week
5. ✅ **Calculate score** - Week 5
6. ✅ **BUILD or KILL** - Based on 60+ threshold

---

**🚀 Start with competitive intelligence. Know your market. Win.**

**Repository:** https://github.com/breverdbidder/validate-build-system  
**Status:** Production-ready ✅  
**Last Updated:** December 31, 2025
