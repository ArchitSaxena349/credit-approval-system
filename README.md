# Credit Approval System

A Django-based REST API system for credit approval based on customer data and loan history. This system provides endpoints for customer registration, loan eligibility checking, loan creation, and loan management.

## Features

- **Customer Management**: Register new customers with automatic credit limit calculation
- **Credit Scoring**: Advanced credit scoring algorithm based on loan history
- **Loan Eligibility**: Check loan eligibility with interest rate correction
- **Loan Management**: Create and view loans with comprehensive tracking
- **Background Tasks**: Celery-based background processing for data ingestion
- **Docker Support**: Fully containerized application with PostgreSQL and Redis

## Tech Stack

- Django 4.2+
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Docker & Docker Compose

## Project Structure

```
credit_approval_system/
├── credit_approval/          # Main Django project
│   ├── settings.py          # Django settings with Celery config
│   ├── celery.py           # Celery configuration
│   └── urls.py             # Main URL configuration
├── loans/                   # Main application
│   ├── models.py           # Customer and Loan models
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # API views
│   ├── utils.py            # Credit scoring utilities
│   ├── tasks.py            # Celery background tasks
│   ├── admin.py            # Django admin configuration
│   └── management/commands/ # Management commands
├── requirements.txt         # Python dependencies
├── docker-compose.yml      # Docker services configuration
├── Dockerfile              # Docker image configuration
└── README.md               # This file
```

## Setup and Installation

### Option 1: Docker Setup (Recommended)

1. **Clone the repository and navigate to the project directory**
   ```bash
   cd credit_approval_system
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Create superuser (optional)**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

### Option 2: Local Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL and Redis**
   - Install PostgreSQL and create a database named `credit_approval`
   - Install Redis and ensure it's running on port 6379

3. **Configure environment variables**
   Create a `.env` file with:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/credit_approval
   REDIS_URL=redis://localhost:6379/0
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Start Celery worker (in separate terminal)**
   ```bash
   celery -A credit_approval worker --loglevel=info
   ```

## API Endpoints

### 1. Register Customer
**POST** `/register/`

Register a new customer with automatic credit limit calculation.

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "age": 30,
  "monthly_income": 50000,
  "phone_number": "1234567890"
}
```

**Response:**
```json
{
  "customer_id": 1,
  "name": "John Doe",
  "age": 30,
  "monthly_income": 50000,
  "approved_limit": 1800000,
  "phone_number": "1234567890"
}
```

### 2. Check Loan Eligibility
**POST** `/check-eligibility/`

Check if a customer is eligible for a loan and get corrected interest rate.

**Request Body:**
```json
{
  "customer_id": 1,
  "loan_amount": 100000,
  "interest_rate": 8.0,
  "tenure": 12
}
```

**Response:**
```json
{
  "customer_id": 1,
  "approval": true,
  "interest_rate": 8.0,
  "corrected_interest_rate": 8.0,
  "tenure": 12,
  "monthly_installment": 8698.84
}
```

### 3. Create Loan
**POST** `/create-loan/`

Create a new loan if the customer is eligible.

**Request Body:**
```json
{
  "customer_id": 1,
  "loan_amount": 100000,
  "interest_rate": 8.0,
  "tenure": 12
}
```

**Response:**
```json
{
  "loan_id": 1,
  "customer_id": 1,
  "loan_approved": true,
  "message": "Loan approved successfully",
  "monthly_installment": 8698.84
}
```

### 4. View Loan Details
**GET** `/view-loan/{loan_id}/`

Get details of a specific loan.

**Response:**
```json
{
  "loan_id": 1,
  "customer": {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "1234567890",
    "age": 30
  },
  "loan_amount": 100000,
  "interest_rate": 8.0,
  "monthly_repayment": 8698.84,
  "tenure": 12
}
```

### 5. View Customer Loans
**GET** `/view-loans/{customer_id}/`

Get all loans for a specific customer.

**Response:**
```json
[
  {
    "loan_id": 1,
    "loan_amount": 100000,
    "interest_rate": 8.0,
    "monthly_installment": 8698.84,
    "repayments_left": 12
  }
]
```

## Credit Scoring Algorithm

The system uses a sophisticated credit scoring algorithm with the following components:

1. **Past Loans Paid on Time (35% weight)**
   - Calculates the ratio of EMIs paid on time vs total EMIs

2. **Number of Loans Taken (20% weight)**
   - Fewer loans result in higher scores
   - ≤2 loans: 20 points, ≤5 loans: 15 points, etc.

3. **Loan Activity in Current Year (20% weight)**
   - Recent loan activity affects score
   - No current year loans: 20 points, ≤2 loans: 15 points, etc.

4. **Loan Volume vs Approved Limit (25% weight)**
   - Compares total loan amount to approved credit limit
   - Lower utilization results in higher scores

5. **Special Conditions**
   - If current debt > approved limit: score = 0
   - If total EMIs > 50% of monthly salary: loan rejected

## Interest Rate Slabs

Based on credit score:
- **Score > 50**: Approve at requested rate
- **30 < Score ≤ 50**: Minimum 12% interest rate
- **10 < Score ≤ 30**: Minimum 16% interest rate
- **Score ≤ 10**: Reject loan

## Data Ingestion

The system supports background data ingestion from Excel files using Celery.

### Using Management Command

```bash
# Synchronous ingestion
python manage.py ingest_data --customer-file customer_data.xlsx --loan-file loan_data.xlsx

# Asynchronous ingestion (requires Celery worker)
python manage.py ingest_data --customer-file customer_data.xlsx --loan-file loan_data.xlsx --async
```

### Expected Excel File Formats

**Customer Data (customer_data.xlsx):**
- customer_id
- first_name
- last_name
- phone_number
- monthly_salary
- approved_limit
- current_debt

**Loan Data (loan_data.xlsx):**
- customer_id
- loan_id
- loan_amount
- tenure
- interest_rate
- monthly_repayment
- emis_paid_on_time
- start_date
- end_date

## Testing

Use the provided sample data files for testing:
- `sample_customer_data.csv`
- `sample_loan_data.csv`

## Django Admin

Access the Django admin interface at `/admin/` to manage customers and loans directly.

## Development

### Running Tests
```bash
python manage.py test
```

### Code Quality
The project follows Django best practices with:
- Proper model relationships
- Serializer validation
- Error handling
- Background task processing
- Dockerized deployment

## Production Considerations

1. **Environment Variables**: Use proper secret management
2. **Database**: Configure PostgreSQL with proper backup strategy
3. **Caching**: Implement Redis caching for frequently accessed data
4. **Monitoring**: Add logging and monitoring solutions
5. **Security**: Implement proper authentication and authorization
6. **Scaling**: Use load balancers and multiple worker processes

## License

This project is developed by Archit Saxena.
