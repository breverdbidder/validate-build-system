#!/usr/bin/env python3
"""
Competitive Intelligence via SimilarWeb (Apify API)
Bypasses SimilarWeb paywall using API Mega Library credentials

Usage:
    python3 analyze_competitors.py \
        --domains "dealcheck.io,zilculator.com" \
        --output results/analysis_20251231.json

Requirements:
    - APIFY_API_TOKEN environment variable or --token argument
    - requests library: pip install requests
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime

try:
    import requests
except ImportError:
    print("❌ Error: 'requests' library not found")
    print("Install with: pip install requests")
    sys.exit(1)


def analyze_competitors(domains, apify_token=None):
    """
    Scrape SimilarWeb data for multiple competitors
    
    Args:
        domains (list): List of domain names (without https://)
        apify_token (str): Apify API token (optional, will use env var if not provided)
    
    Returns:
        dict: Structured competitor data
    """
    
    # Get token from env if not provided
    if not apify_token:
        apify_token = os.getenv('APIFY_API_TOKEN')
    
    if not apify_token:
        raise ValueError("APIFY_API_TOKEN not set. Export it or pass via --token")
    
    # Apify SimilarWeb scraper (free tier)
    ACTOR_ID = "mscraper~similarweb-quick-scraper"
    
    # Prepare input
    input_data = {"websites": domains}
    
    print("="*80)
    print("🔓 BYPASSING SIMILARWEB PAYWALL VIA APIFY API")
    print("="*80)
    print(f"\n🎯 Analyzing {len(domains)} competitors:")
    for domain in domains:
        print(f"   • {domain}")
    print()
    
    # Start scraper run
    run_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs"
    response = requests.post(
        run_url,
        params={"token": apify_token},
        json=input_data
    )
    
    if response.status_code != 201:
        print(f"❌ Error starting scraper: {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    run_data = response.json()['data']
    run_id = run_data['id']
    dataset_id = run_data['defaultDatasetId']
    
    print(f"✅ Run ID: {run_id}")
    print(f"📊 Dataset ID: {dataset_id}")
    print(f"\n⏳ Waiting for results (30-60 seconds)...\n")
    
    # Poll for completion
    while True:
        status_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs/{run_id}"
        status_resp = requests.get(status_url, params={"token": apify_token})
        
        if status_resp.status_code == 200:
            status = status_resp.json()['data']['status']
            print(f"   Status: {status}...", end='\r')
            
            if status in ['SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT']:
                print(f"\n   Final Status: {status}")
                break
        
        time.sleep(5)
    
    if status != 'SUCCEEDED':
        print(f"\n❌ Scraper failed with status: {status}")
        sys.exit(1)
    
    # Retrieve results
    print(f"\n📥 Retrieving data...")
    results_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items"
    results_resp = requests.get(results_url, params={"token": apify_token})
    
    if results_resp.status_code != 200:
        print(f"❌ Error fetching results: {results_resp.status_code}")
        sys.exit(1)
    
    results = results_resp.json()
    print(f"✅ Retrieved {len(results)} results!\n")
    
    # Structure data
    structured_data = {
        "metadata": {
            "scraped_at": datetime.utcnow().isoformat(),
            "scraper": ACTOR_ID,
            "num_competitors": len(results),
            "cost": "$0 (Apify free tier)"
        },
        "competitors": []
    }
    
    for result in results:
        domain = result.get('domain', result.get('SiteName', 'Unknown'))
        engagements = result.get('Engagments', {})
        monthly_visits = result.get('EstimatedMonthlyVisits', {})
        
        competitor_data = {
            "domain": domain,
            "rankings": {
                "global_rank": result.get('GlobalRank', {}).get('Rank'),
                "country_rank": result.get('CountryRank', {}).get('Rank'),
                "country_code": result.get('CountryRank', {}).get('CountryCode', 'US'),
                "category": result.get('Category', 'N/A'),
                "category_rank": result.get('CategoryRank', {}).get('Rank')
            },
            "traffic": {
                "monthly_visits": monthly_visits,
                "current_visits": int(engagements.get('Visits', 0)) if engagements.get('Visits') else None,
                "current_month": f"{engagements.get('Year', '')}-{engagements.get('Month', '').zfill(2)}" if engagements.get('Month') else None
            },
            "engagement": {
                "bounce_rate": float(engagements.get('BounceRate', 0)) * 100 if engagements.get('BounceRate') else None,
                "pages_per_visit": float(engagements.get('PagePerVisit', 0)) if engagements.get('PagePerVisit') else None,
                "time_on_site_seconds": float(engagements.get('TimeOnSite', 0)) if engagements.get('TimeOnSite') else None
            },
            "traffic_sources": result.get('TrafficSources', {}),
            "top_countries": result.get('TopCountryShares', [])[:5],
            "description": result.get('Description', ''),
            "raw_data": result  # Keep full SimilarWeb response for reference
        }
        
        structured_data["competitors"].append(competitor_data)
    
    return structured_data


def main():
    parser = argparse.ArgumentParser(
        description="Analyze competitors using SimilarWeb data via Apify API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze 2 competitors
  python3 analyze_competitors.py --domains "dealcheck.io,zilculator.com" --output results/analysis.json
  
  # Analyze 4 competitors with custom token
  python3 analyze_competitors.py \\
    --domains "propertyonion.com,rehabvaluator.com,dealcheck.io,zilculator.com" \\
    --token apify_api_xxxxx \\
    --output results/all_competitors.json
        """
    )
    parser.add_argument(
        '--domains',
        required=True,
        help='Comma-separated list of domains (e.g., "dealcheck.io,zilculator.com")'
    )
    parser.add_argument(
        '--token',
        help='Apify API token (optional, uses APIFY_API_TOKEN env var if not provided)'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Output JSON file path (e.g., results/analysis_20251231.json)'
    )
    
    args = parser.parse_args()
    
    # Parse domains
    domains = [d.strip() for d in args.domains.split(',')]
    
    # Analyze competitors
    try:
        data = analyze_competitors(domains, args.token)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    
    # Save results
    with open(args.output, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n💾 Results saved to: {args.output}")
    print("="*80)
    
    # Print summary
    print("\n📊 QUICK SUMMARY:")
    print(f"{'='*80}")
    for competitor in data["competitors"]:
        domain = competitor["domain"]
        visits = competitor["traffic"]["current_visits"]
        bounce = competitor["engagement"]["bounce_rate"]
        pages = competitor["engagement"]["pages_per_visit"]
        time_sec = competitor["engagement"]["time_on_site_seconds"]
        
        print(f"\n🌐 {domain.upper()}")
        print(f"   Monthly Visits: {visits:,}" if visits else "   Monthly Visits: N/A")
        print(f"   Bounce Rate: {bounce:.1f}%" if bounce else "   Bounce Rate: N/A")
        print(f"   Pages/Visit: {pages:.2f}" if pages else "   Pages/Visit: N/A")
        
        if time_sec:
            minutes = int(time_sec // 60)
            seconds = int(time_sec % 60)
            print(f"   Time on Site: {minutes}m {seconds}s")
        else:
            print(f"   Time on Site: N/A")
    
    print(f"\n{'='*80}")
    print(f"✅ Analysis complete! Use generate_summary.py to create exec summary.")
    print("="*80)


if __name__ == "__main__":
    main()
