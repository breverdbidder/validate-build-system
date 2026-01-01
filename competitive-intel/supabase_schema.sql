-- Competitive Intelligence Database Schema
-- Tracks competitor analysis over time for trend monitoring

-- Table 1: Competitor Snapshots (time-series data)
CREATE TABLE IF NOT EXISTS competitor_snapshots (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Competitor identification
    domain TEXT NOT NULL,
    product_name TEXT,
    
    -- Traffic metrics
    monthly_visits INTEGER,
    visits_month TEXT, -- e.g., "2025-11"
    
    -- Engagement metrics
    bounce_rate NUMERIC(5,2), -- e.g., 38.50 for 38.5%
    pages_per_visit NUMERIC(5,2),
    time_on_site_seconds INTEGER,
    
    -- Rankings
    global_rank INTEGER,
    country_rank INTEGER,
    country_code TEXT DEFAULT 'US',
    category TEXT,
    category_rank INTEGER,
    
    -- Traffic sources (percentages)
    direct_traffic NUMERIC(5,2),
    search_traffic NUMERIC(5,2),
    social_traffic NUMERIC(5,2),
    referral_traffic NUMERIC(5,2),
    paid_traffic NUMERIC(5,2),
    mail_traffic NUMERIC(5,2),
    
    -- Metadata
    scraped_at TIMESTAMP WITH TIME ZONE,
    scraper_version TEXT DEFAULT 'v1.0',
    raw_data JSONB, -- Full SimilarWeb response
    
    -- Indexing for fast queries
    UNIQUE(domain, visits_month)
);

-- Table 2: Competitive Analysis Reports
CREATE TABLE IF NOT EXISTS competitive_analyses (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Analysis metadata
    analysis_name TEXT NOT NULL,
    product_name TEXT NOT NULL,
    product_focus TEXT,
    
    -- Targets
    target_users INTEGER,
    target_arpu INTEGER,
    target_arr INTEGER,
    
    -- Market metrics (calculated)
    total_market_visits INTEGER,
    num_competitors INTEGER,
    required_monthly_visits INTEGER,
    market_penetration_pct NUMERIC(5,2),
    
    -- Report files
    report_path TEXT, -- Path to markdown file
    data_path TEXT, -- Path to JSON file
    
    -- Strategic insights
    key_findings TEXT[],
    recommendations TEXT[],
    validation_score INTEGER, -- 0-100
    
    UNIQUE(analysis_name, created_at::DATE)
);

-- Table 3: Competitor Trends (derived view)
CREATE VIEW competitor_trends AS
SELECT 
    domain,
    DATE_TRUNC('month', created_at) as month,
    AVG(monthly_visits) as avg_visits,
    AVG(bounce_rate) as avg_bounce_rate,
    AVG(pages_per_visit) as avg_pages_per_visit,
    COUNT(*) as snapshot_count
FROM competitor_snapshots
GROUP BY domain, DATE_TRUNC('month', created_at)
ORDER BY domain, month DESC;

-- Table 4: Market Share Analysis (derived view)
CREATE VIEW market_share AS
SELECT 
    visits_month,
    domain,
    monthly_visits,
    SUM(monthly_visits) OVER (PARTITION BY visits_month) as total_market,
    ROUND(
        (monthly_visits::NUMERIC / NULLIF(SUM(monthly_visits) OVER (PARTITION BY visits_month), 0)) * 100,
        2
    ) as market_share_pct
FROM competitor_snapshots
WHERE monthly_visits IS NOT NULL
ORDER BY visits_month DESC, monthly_visits DESC;

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_competitor_domain ON competitor_snapshots(domain);
CREATE INDEX IF NOT EXISTS idx_competitor_month ON competitor_snapshots(visits_month);
CREATE INDEX IF NOT EXISTS idx_competitor_created ON competitor_snapshots(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_analysis_product ON competitive_analyses(product_name);
CREATE INDEX IF NOT EXISTS idx_analysis_created ON competitive_analyses(created_at DESC);

-- Row Level Security (RLS)
ALTER TABLE competitor_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE competitive_analyses ENABLE ROW LEVEL SECURITY;

-- Allow authenticated users to read/write
CREATE POLICY "Allow authenticated users full access to competitor_snapshots"
    ON competitor_snapshots
    FOR ALL
    TO authenticated
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Allow authenticated users full access to competitive_analyses"
    ON competitive_analyses
    FOR ALL
    TO authenticated
    USING (true)
    WITH CHECK (true);

-- Comments for documentation
COMMENT ON TABLE competitor_snapshots IS 'Time-series competitor traffic data from SimilarWeb';
COMMENT ON TABLE competitive_analyses IS 'Competitive intelligence reports and metadata';
COMMENT ON VIEW competitor_trends IS 'Monthly aggregated competitor metrics';
COMMENT ON VIEW market_share IS 'Relative market share calculations by month';
