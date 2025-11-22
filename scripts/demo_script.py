#!/usr/bin/env python3
"""
Credit Approval System - API Demo Script
Run this after starting the Django server to test all endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_separator(title):
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def make_request(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        
        print(f"\n🔗 {method} {endpoint}")
        if data:
            print(f"📤 Request: {json.dumps(data, indent=2)}")
        
        print(f"📊 Status: {response.status_code}")
        
        try:
            response_data = response.json()
            print(f"📨 Response: {json.dumps(response_data, indent=2)}")
            return response_data
        except:
            print(f"📨 Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to server. Make sure Django server is running!")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def main():
    print("🚀 Credit Approval System - API Demo")
    print("📝 Make sure the Django server is running: python manage.py runserver")
    print("⏳ Starting demo in 3 seconds...")
    time.sleep(3)
    
    # 1. Customer Registration
    print_separator("1. Customer Registration")
    customer_data = {
        "first_name": "John",
        "last_name": "Doe",
        "age": 30,
        "monthly_income": 75000,
        "phone_number": "9876543210"
    }
    customer_response = make_request("POST", "/register/", customer_data)
    
    if not customer_response:
        print("❌ Demo stopped due to server connection issue")
        return
    
    customer_id = customer_response.get("customer_id", 1)
    
    # 2. Check Loan Eligibility
    print_separator("2. Check Loan Eligibility")
    eligibility_data = {
        "customer_id": customer_id,
        "loan_amount": 200000,
        "interest_rate": 10.0,
        "tenure": 24
    }
    eligibility_response = make_request("POST", "/check-eligibility/", eligibility_data)
    
    # 3. Create Loan
    print_separator("3. Create Loan")
    loan_data = {
        "customer_id": customer_id,
        "loan_amount": 200000,
        "interest_rate": 10.0,
        "tenure": 24
    }
    loan_response = make_request("POST", "/create-loan/", loan_data)
    
    if loan_response:
        loan_id = loan_response.get("loan_id", 1)
    else:
        loan_id = 1  # Fallback for demo
    
    # 4. View Loan Details
    print_separator("4. View Loan Details")
    make_request("GET", f"/view-loan/{loan_id}/")
    
    # 5. View Customer Loans
    print_separator("5. View Customer Loans")
    make_request("GET", f"/view-loans/{customer_id}/")
    
    # Demo with existing customer (if any)
    print_separator("6. Demo with Existing Customer (ID: 1)")
    make_request("GET", "/view-loans/1/")
    
    print_separator("Demo Complete! 🎉")
    print("✅ All API endpoints have been tested")
    print("🎥 You can now record your video demo using these same requests")
    print("📚 Check SUBMISSION_GUIDE.md for detailed instructions")

if __name__ == "__main__":
    main()
