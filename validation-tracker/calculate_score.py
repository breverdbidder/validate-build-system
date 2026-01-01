#!/usr/bin/env python3
"""
Calculate validation score for a tool
"""
import os
import sys
import argparse
from supabase import create_client, Client

def calculate_score(tool_name):
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("❌ Error: Set SUPABASE_URL and SUPABASE_KEY in .env")
        return
    
    supabase: Client = create_client(url, key)
    
    # Get metrics from database
    visitors = supabase.table("visitors").select("*").eq("tool", tool_name).execute()
    cta_clicks = supabase.table("cta_clicks").select("*").eq("tool", tool_name).execute()
    interviews = supabase.table("interviews").select("*").eq("tool", tool_name).execute()
    
    visitor_count = len(visitors.data) if visitors.data else 0
    cta_count = len(cta_clicks.data) if cta_clicks.data else 0
    interview_count = len(interviews.data) if interviews.data else 0
    
    # Calculate metrics
    cta_conversion = (cta_count / visitor_count * 100) if visitor_count > 0 else 0
    
    would_pay_count = sum(1 for i in interviews.data if i.get('would_pay')) if interviews.data else 0
    would_pay_pct = (would_pay_count / interview_count * 100) if interview_count > 0 else 0
    
    # Quantitative score (out of 400)
    visitor_score = min(visitor_count / 5, 100)  # 500 visits = 100 points
    cta_score = min(cta_conversion * 10, 100)  # 10% conversion = 100 points
    interview_score = min(interview_count * 5, 100)  # 20 interviews = 100 points
    would_pay_score = min(would_pay_pct / 0.3, 100)  # 30% = 100 points
    
    quantitative_total = int(visitor_score + cta_score + interview_score + would_pay_score)
    
    # Qualitative score (out of 100)
    high_urgency = sum(1 for i in interviews.data if i.get('urgency') == 'High') if interviews.data else 0
    qualitative_total = min(high_urgency * 10, 100)
    
    # Total score
    total_score = quantitative_total + qualitative_total
    percentage = (total_score / 500) * 100
    
    # Determine status
    if percentage >= 60:
        status = "✅ GREEN - PROCEED TO BUILD"
        color = "\033[92m"  # Green
    elif percentage >= 40:
        status = "🟡 YELLOW - PIVOT REQUIRED"
        color = "\033[93m"  # Yellow
    else:
        status = "🔴 RED - KILL PROJECT"
        color = "\033[91m"  # Red
    reset = "\033[0m"
    
    # Print results
    print("=" * 60)
    print(f"VALIDATION SCORECARD: {tool_name}")
    print("=" * 60)
    print(f"\nQUANTITATIVE METRICS:")
    print(f"  Landing page visits: {visitor_count} ({int(visitor_score)}/100)")
    print(f"  CTA conversion: {cta_conversion:.1f}% ({int(cta_score)}/100)")
    print(f"  User interviews: {interview_count} ({int(interview_score)}/100)")
    print(f"  Would pay %: {would_pay_pct:.1f}% ({int(would_pay_score)}/100)")
    print(f"  Subtotal: {quantitative_total}/400")
    
    print(f"\nQUALITATIVE SIGNALS:")
    print(f"  High urgency: {high_urgency}")
    print(f"  Subtotal: {qualitative_total}/100")
    
    print(f"\nTOTAL SCORE: {total_score}/500 ({percentage:.0f}%)")
    print(f"STATUS: {color}{status}{reset}")
    
    if percentage >= 60:
        print(f"\n💡 DECISION: Build MVP immediately")
        print(f"   ESTIMATED TIME TO $3K/MONTH: 3-4 months")
    elif percentage >= 40:
        print(f"\n💡 DECISION: Pivot pricing or target market, re-validate")
    else:
        print(f"\n💡 DECISION: Kill project, move to next tool")
    
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate validation score")
    parser.add_argument("--tool", required=True, choices=["Zoning Analyst", "Lien Discovery"])
    args = parser.parse_args()
    calculate_score(args.tool)
