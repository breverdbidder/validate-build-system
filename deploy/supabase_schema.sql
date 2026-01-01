-- Validation Automation System Database Schema
-- Supabase PostgreSQL

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Visitors table (landing page traffic)
CREATE TABLE IF NOT EXISTS visitors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tool VARCHAR(50) NOT NULL, -- 'Zoning Analyst' or 'Lien Discovery'
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    page_url TEXT,
    referrer TEXT,
    user_agent TEXT,
    ip_address INET,
    session_id VARCHAR(100)
);

-- CTA Clicks table
CREATE TABLE IF NOT EXISTS cta_clicks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tool VARCHAR(50) NOT NULL,
    cta_tier VARCHAR(20) NOT NULL, -- 'primary', 'secondary', 'tertiary'
    cta_text TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    session_id VARCHAR(100)
);

-- Interviews table
CREATE TABLE IF NOT EXISTS interviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tool VARCHAR(50) NOT NULL,
    contact_name VARCHAR(200),
    contact_company VARCHAR(200),
    contact_email VARCHAR(200),
    contact_phone VARCHAR(50),
    interview_date DATE,
    pain_score INTEGER CHECK (pain_score >= 1 AND pain_score <= 10),
    would_pay BOOLEAN,
    payment_amount DECIMAL(10,2),
    urgency VARCHAR(20), -- 'High', 'Medium', 'Low'
    hoa_experience TEXT,
    notes TEXT,
    recorded BOOLEAN DEFAULT FALSE,
    recording_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Validation Scores table
CREATE TABLE IF NOT EXISTS validation_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tool VARCHAR(50) NOT NULL,
    calculation_date DATE DEFAULT CURRENT_DATE,
    
    -- Quantitative metrics
    landing_page_visits INTEGER DEFAULT 0,
    cta_conversion_rate DECIMAL(5,2) DEFAULT 0.00,
    interview_count INTEGER DEFAULT 0,
    would_pay_percentage DECIMAL(5,2) DEFAULT 0.00,
    
    -- Qualitative signals
    feature_requests INTEGER DEFAULT 0,
    urgency_count INTEGER DEFAULT 0,
    referrals INTEGER DEFAULT 0,
    
    -- Warning signals
    no_urgency_count INTEGER DEFAULT 0,
    price_sensitivity_count INTEGER DEFAULT 0,
    
    -- Calculated scores
    quantitative_score INTEGER DEFAULT 0,
    qualitative_score INTEGER DEFAULT 0,
    total_score INTEGER DEFAULT 0,
    percentage DECIMAL(5,2) DEFAULT 0.00,
    status VARCHAR(20), -- 'GREEN', 'YELLOW', 'RED'
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX idx_visitors_tool ON visitors(tool);
CREATE INDEX idx_visitors_timestamp ON visitors(timestamp);
CREATE INDEX idx_cta_clicks_tool ON cta_clicks(tool);
CREATE INDEX idx_interviews_tool ON interviews(tool);
CREATE INDEX idx_validation_scores_tool ON validation_scores(tool);

-- Create view for dashboard
CREATE OR REPLACE VIEW validation_dashboard AS
SELECT 
    i.tool,
    COUNT(DISTINCT v.session_id) as total_visitors,
    COUNT(c.id) as total_cta_clicks,
    ROUND(COUNT(c.id)::DECIMAL / NULLIF(COUNT(DISTINCT v.session_id), 0) * 100, 2) as cta_conversion_rate,
    COUNT(i.id) as interview_count,
    ROUND(SUM(CASE WHEN i.would_pay THEN 1 ELSE 0 END)::DECIMAL / NULLIF(COUNT(i.id), 0) * 100, 2) as would_pay_percentage,
    ROUND(AVG(i.pain_score), 1) as avg_pain_score,
    COUNT(CASE WHEN i.urgency = 'High' THEN 1 END) as high_urgency_count
FROM 
    interviews i
LEFT JOIN visitors v ON v.tool = i.tool
LEFT JOIN cta_clicks c ON c.tool = i.tool
GROUP BY i.tool;

-- Insert sample data for testing
-- (Optional - comment out in production)
-- INSERT INTO visitors (tool, session_id) VALUES 
--     ('Zoning Analyst', 'session_001'),
--     ('Lien Discovery', 'session_002');

