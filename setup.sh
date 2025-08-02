#!/bin/bash

# Credit Approval System Setup Script

echo "Setting up Credit Approval System..."

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo "Creating superuser (optional)..."
echo "You can skip this by pressing Ctrl+C"
python manage.py createsuperuser

# Run tests
echo "Running tests..."
python manage.py test

echo "Setup complete!"
echo ""
echo "To start the development server:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Start Django server: python manage.py runserver"
echo "3. Start Celery worker (in another terminal): celery -A credit_approval worker --loglevel=info"
echo ""
echo "API endpoints will be available at:"
echo "- POST /register/ - Register customer"
echo "- POST /check-eligibility/ - Check loan eligibility"
echo "- POST /create-loan/ - Create loan"
echo "- GET /view-loan/{loan_id}/ - View loan details"
echo "- GET /view-loans/{customer_id}/ - View customer loans"
echo ""
echo "Admin interface: http://localhost:8000/admin/"
