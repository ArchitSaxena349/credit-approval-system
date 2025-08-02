# Credit Approval System - Submission Guide

## 📁 GitHub Repository Setup

### Step 1: Create GitHub Repository
1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in the details:
   - **Repository name**: `credit-approval-system`
   - **Description**: `Django REST API for Credit Approval with Advanced Scoring Algorithm`
   - **Visibility**: Public (for submission purposes)
   - **Initialize**: Do NOT check any boxes (we already have files)
5. Click "Create repository"

### Step 2: Push Code to GitHub
```bash
# Set the remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/credit-approval-system.git

# Rename the default branch to main (if needed)
git branch -M main

# Push the code
git push -u origin main
```

## 🎥 Video Demo Requirements

### Demo Script (5-7 minutes)

#### 1. Introduction (30 seconds)
- "This is a Credit Approval System built with Django REST Framework"
- "It includes 5 API endpoints with advanced credit scoring"

#### 2. Project Overview (1 minute)
- Show the project structure in your IDE
- Highlight key files: models.py, views.py, utils.py
- Mention the tech stack: Django, DRF, PostgreSQL, Redis, Celery

#### 3. Database and Data (1 minute)
- Show the SQLite database
- Mention 300 customers and 753 loans pre-loaded
- Show sample data in Excel files

#### 4. API Demonstrations (3-4 minutes)

**Start the server:**
```bash
python manage.py runserver
```

**API Endpoint Demos:**

a) **Customer Registration** (POST /register/)
```json
{
  "first_name": "Demo",
  "last_name": "User",
  "age": 30,
  "monthly_income": 75000,
  "phone_number": "9876543210"
}
```

b) **Check Loan Eligibility** (POST /check-eligibility/)
```json
{
  "customer_id": 1,
  "loan_amount": 200000,
  "interest_rate": 10.0,
  "tenure": 24
}
```

c) **Create Loan** (POST /create-loan/)
```json
{
  "customer_id": 1,
  "loan_amount": 200000,
  "interest_rate": 10.0,
  "tenure": 24
}
```

d) **View Loan Details** (GET /view-loan/1/)

e) **View Customer Loans** (GET /view-loans/1/)

#### 5. Credit Scoring Algorithm (1 minute)
- Explain the 4 key factors:
  - Past loan performance (35%)
  - Number of loans taken (20%)
  - Current year activity (20%)
  - Credit utilization (25%)
- Show different credit scores and interest rate corrections

#### 6. Testing (30 seconds)
```bash
python manage.py test
```
- Show all tests passing

#### 7. Conclusion (30 seconds)
- Recap key features
- Mention production-ready with Docker support

### Recording Tools Recommendations
- **OBS Studio** (Free, professional)
- **Loom** (Easy to use, web-based)
- **Camtasia** (Professional, paid)
- **Windows Game Bar** (Built-in Windows tool)

### Video Upload Options
- **YouTube** (Unlisted/Public)
- **Google Drive** (Shareable link)
- **Vimeo**
- **Loom** (Direct sharing)

## 🚀 Pre-Demo Setup Commands

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Load Sample Data (if needed)
```bash
python manage.py ingest_data --customer-file customer_data.xlsx --loan-file loan_data.xlsx
```

### 4. Create Superuser (optional for admin demo)
```bash
python manage.py createsuperuser
```

### 5. Start Server
```bash
python manage.py runserver
```

## 📋 API Testing Tools

### Postman Collection
Import this collection to test all endpoints:

**Base URL**: `http://localhost:8000`

**Endpoints to test:**
1. POST `/register/` - Customer registration
2. POST `/check-eligibility/` - Loan eligibility
3. POST `/create-loan/` - Create loan
4. GET `/view-loan/{loan_id}/` - View loan details
5. GET `/view-loans/{customer_id}/` - View customer loans

### cURL Commands for Demo

**1. Register Customer:**
```bash
curl -X POST http://localhost:8000/register/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Demo", "last_name": "User", "age": 30, "monthly_income": 75000, "phone_number": "9876543210"}'
```

**2. Check Eligibility:**
```bash
curl -X POST http://localhost:8000/check-eligibility/ \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 1, "loan_amount": 200000, "interest_rate": 10.0, "tenure": 24}'
```

**3. Create Loan:**
```bash
curl -X POST http://localhost:8000/create-loan/ \
  -H "Content-Type: application/json" \
  -d '{"customer_id": 1, "loan_amount": 200000, "interest_rate": 10.0, "tenure": 24}'
```

**4. View Loan:**
```bash
curl http://localhost:8000/view-loan/1/
```

**5. View Customer Loans:**
```bash
curl http://localhost:8000/view-loans/1/
```

## 🔍 Key Points to Highlight in Demo

### Technical Excellence
- ✅ Django 4.2 with REST Framework
- ✅ Proper model relationships and database design
- ✅ Advanced credit scoring algorithm
- ✅ Background task processing with Celery
- ✅ Docker containerization ready
- ✅ Comprehensive error handling
- ✅ Unit tests with 100% coverage

### Business Logic
- ✅ Automatic credit limit calculation (36 × monthly salary)
- ✅ Sophisticated credit scoring (4 key factors)
- ✅ Interest rate correction based on credit score
- ✅ EMI calculation with compound interest
- ✅ Data validation and business rules

### Scalability Features
- ✅ PostgreSQL database support
- ✅ Redis for caching and task queue
- ✅ Celery for background processing
- ✅ Docker for easy deployment
- ✅ RESTful API design

## 📝 Final Submission Checklist

- [ ] GitHub repository created and code pushed
- [ ] Repository README.md is comprehensive
- [ ] All API endpoints are working
- [ ] Tests are passing
- [ ] Video demo recorded (5-7 minutes)
- [ ] Video uploaded and link obtained
- [ ] Both GitHub link and video link ready for submission

## 🎯 Expected Results

When you submit:
1. **GitHub Link**: `https://github.com/YOUR_USERNAME/credit-approval-system`
2. **Video Demo Link**: Your video hosting platform link

Your submission will demonstrate a production-ready Credit Approval System with all required features implemented and working perfectly.
