#!/bin/bash

echo "🚀 Deploying Validation Automation System"
echo ""

# Check if Cloudflare CLI is installed
if ! command -v wrangler &> /dev/null; then
    echo "❌ Cloudflare Wrangler not installed"
    echo "   Install: npm install -g wrangler"
    exit 1
fi

# Deploy Zoning Analyst landing page
echo "📦 Deploying Zoning Analyst landing page..."
cd landing-pages/zoning-analyst
wrangler pages deploy . --project-name=validate-zoning
echo "✅ Deployed to: https://validate-zoning.pages.dev"
cd ../..

# Deploy Lien Discovery landing page
echo "📦 Deploying Lien Discovery landing page..."
cd landing-pages/lien-discovery
wrangler pages deploy . --project-name=validate-lien
echo "✅ Deployed to: https://validate-lien.pages.dev"
cd ../..

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Set up Supabase database (run deploy/supabase_schema.sql)"
echo "2. Add SUPABASE_URL and SUPABASE_KEY to .env"
echo "3. Start tracking interviews with validation-tracker/add_interview.py"
