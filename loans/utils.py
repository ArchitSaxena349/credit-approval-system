from decimal import Decimal
from datetime import datetime, date
from django.db.models import Sum, Count, Q
from .models import Customer, Loan
import math


def calculate_monthly_installment(loan_amount, annual_interest_rate, tenure_months):
    """
    Calculate monthly installment using compound interest formula
    EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
    """
    if annual_interest_rate == 0:
        return loan_amount / tenure_months
    
    monthly_rate = annual_interest_rate / (12 * 100)  # Convert annual % to monthly decimal
    
    # Calculate EMI using compound interest formula
    numerator = loan_amount * monthly_rate * ((1 + monthly_rate) ** tenure_months)
    denominator = ((1 + monthly_rate) ** tenure_months) - 1
    
    return numerator / denominator


def calculate_credit_score(customer_id):
    """
    Calculate credit score based on:
    1. Past Loans paid on time (35% weight)
    2. Number of loans taken in past (20% weight)
    3. Loan activity in current year (20% weight)
    4. Loan approved volume vs limit (25% weight)
    """
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return 0
    
    loans = Loan.objects.filter(customer=customer)
    
    if not loans.exists():
        return 85  # New customer, give benefit of doubt
    
    # Component 1: Past loans paid on time (35% weight)
    total_loans = loans.count()
    total_emis = loans.aggregate(total=Sum('tenure'))['total'] or 0
    total_paid_on_time = loans.aggregate(total=Sum('emis_paid_on_time'))['total'] or 0
    
    on_time_score = (total_paid_on_time / max(total_emis, 1)) * 35
    
    # Component 2: Number of loans taken (20% weight) - fewer is better
    if total_loans <= 2:
        loan_count_score = 20
    elif total_loans <= 5:
        loan_count_score = 15
    elif total_loans <= 10:
        loan_count_score = 10
    else:
        loan_count_score = 5
    
    # Component 3: Loan activity in current year (20% weight)
    current_year = datetime.now().year
    current_year_loans = loans.filter(start_date__year=current_year).count()
    
    if current_year_loans == 0:
        current_year_score = 20
    elif current_year_loans <= 2:
        current_year_score = 15
    elif current_year_loans <= 4:
        current_year_score = 10
    else:
        current_year_score = 5
    
    # Component 4: Loan approved volume vs approved limit (25% weight)
    total_loan_amount = loans.aggregate(total=Sum('loan_amount'))['total'] or 0
    if customer.approved_limit > 0:
        volume_ratio = float(total_loan_amount) / float(customer.approved_limit)
        if volume_ratio <= 0.5:
            volume_score = 25
        elif volume_ratio <= 0.75:
            volume_score = 20
        elif volume_ratio <= 1.0:
            volume_score = 15
        else:
            volume_score = 5
    else:
        volume_score = 25
    
    # Calculate final score
    credit_score = on_time_score + loan_count_score + current_year_score + volume_score
    
    # Special condition: If sum of current loans > approved limit, score = 0
    current_debt = customer.current_debt or 0
    if current_debt > customer.approved_limit:
        credit_score = 0
    
    return min(100, max(0, int(credit_score)))


def get_interest_rate_based_on_credit_score(credit_score, requested_rate):
    """
    Determine correct interest rate based on credit score
    """
    if credit_score > 50:
        return requested_rate, requested_rate  # Approve at requested rate
    elif 30 < credit_score <= 50:
        corrected_rate = max(12.0, requested_rate)
        return requested_rate, corrected_rate
    elif 10 < credit_score <= 30:
        corrected_rate = max(16.0, requested_rate)
        return requested_rate, corrected_rate
    else:
        return requested_rate, requested_rate  # Will be rejected anyway


def check_loan_eligibility(customer_id, loan_amount, interest_rate, tenure):
    """
    Check if customer is eligible for loan based on all criteria
    """
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return {
            'eligible': False,
            'credit_score': 0,
            'corrected_interest_rate': interest_rate,
            'monthly_installment': 0,
            'message': 'Customer not found'
        }
    
    # Calculate credit score
    credit_score = calculate_credit_score(customer_id)
    
    # Check if sum of current loans > approved limit
    if customer.current_debt and customer.current_debt > customer.approved_limit:
        return {
            'eligible': False,
            'credit_score': 0,
            'corrected_interest_rate': interest_rate,
            'monthly_installment': 0,
            'message': 'Current debt exceeds approved limit'
        }
    
    # Get corrected interest rate based on credit score
    original_rate, corrected_rate = get_interest_rate_based_on_credit_score(credit_score, float(interest_rate))
    
    # Calculate monthly installment with corrected rate
    monthly_installment = calculate_monthly_installment(
        float(loan_amount), 
        corrected_rate, 
        tenure
    )
    
    # Check if credit score qualifies for loan
    if credit_score <= 10:
        return {
            'eligible': False,
            'credit_score': credit_score,
            'corrected_interest_rate': corrected_rate,
            'monthly_installment': monthly_installment,
            'message': 'Credit score too low'
        }
    
    # Check if sum of all current EMIs > 50% of monthly salary
    current_loans = Loan.objects.filter(
        customer=customer,
        end_date__gte=date.today()
    )
    
    current_emi_sum = sum(float(loan.monthly_repayment) for loan in current_loans)
    max_allowed_emi = float(customer.monthly_salary) * 0.5
    
    if (current_emi_sum + monthly_installment) > max_allowed_emi:
        return {
            'eligible': False,
            'credit_score': credit_score,
            'corrected_interest_rate': corrected_rate,
            'monthly_installment': monthly_installment,
            'message': 'EMI exceeds 50% of monthly salary'
        }
    
    return {
        'eligible': True,
        'credit_score': credit_score,
        'corrected_interest_rate': corrected_rate,
        'monthly_installment': monthly_installment,
        'message': 'Loan approved'
    }
