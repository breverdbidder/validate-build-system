#!/usr/bin/env python3
"""
Add interview to validation tracker
"""
import os
import sys
import argparse
from datetime import date
from supabase import create_client, Client

def add_interview(args):
    # Initialize Supabase
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("❌ Error: SUPABASE_URL and SUPABASE_KEY must be set in .env")
        return False
    
    supabase: Client = create_client(url, key)
    
    # Prepare interview data
    interview_data = {
        "tool": args.tool,
        "contact_name": args.contact,
        "interview_date": args.date or str(date.today()),
        "pain_score": args.pain_score,
        "would_pay": args.would_pay.lower() == "yes",
        "payment_amount": args.amount,
        "urgency": args.urgency,
        "notes": args.notes
    }
    
    # Insert into database
    try:
        response = supabase.table("interviews").insert(interview_data).execute()
        print(f"✅ Interview added successfully!")
        print(f"   Tool: {args.tool}")
        print(f"   Contact: {args.contact}")
        print(f"   Pain Score: {args.pain_score}/10")
        print(f"   Would Pay: {args.would_pay} (${args.amount})")
        return True
    except Exception as e:
        print(f"❌ Error adding interview: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add interview to validation tracker")
    parser.add_argument("--tool", required=True, choices=["Zoning Analyst", "Lien Discovery"])
    parser.add_argument("--contact", required=True, help="Contact name and company")
    parser.add_argument("--pain_score", required=True, type=int, choices=range(1, 11))
    parser.add_argument("--would_pay", required=True, choices=["Yes", "No"])
    parser.add_argument("--amount", type=float, default=0.0)
    parser.add_argument("--urgency", default="Medium", choices=["High", "Medium", "Low"])
    parser.add_argument("--date", help="Interview date (YYYY-MM-DD)")
    parser.add_argument("--notes", default="")
    
    args = parser.parse_args()
    add_interview(args)
