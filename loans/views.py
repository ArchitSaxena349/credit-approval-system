from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from decimal import Decimal
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from .models import Customer, Loan
from .serializers import (
    CustomerRegistrationSerializer,
    CustomerRegistrationResponseSerializer,
    LoanEligibilitySerializer,
    LoanEligibilityResponseSerializer,
    LoanCreateSerializer,
    LoanCreateResponseSerializer,
    LoanDetailSerializer,
    CustomerLoanSerializer
)
from .utils import check_loan_eligibility, calculate_monthly_installment


@api_view(['POST'])
def register_customer(request):
    """
    Register a new customer
    """
    serializer = CustomerRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        customer = serializer.save()
        response_serializer = CustomerRegistrationResponseSerializer(customer)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def check_eligibility(request):
    """
    Check loan eligibility for a customer
    """
    serializer = LoanEligibilitySerializer(data=request.data)
    if serializer.is_valid():
        customer_id = serializer.validated_data['customer_id']
        loan_amount = serializer.validated_data['loan_amount']
        interest_rate = serializer.validated_data['interest_rate']
        tenure = serializer.validated_data['tenure']
        
        # Check eligibility
        eligibility_result = check_loan_eligibility(
            customer_id, loan_amount, interest_rate, tenure
        )
        
        response_data = {
            'customer_id': customer_id,
            'approval': eligibility_result['eligible'],
            'interest_rate': float(interest_rate),
            'corrected_interest_rate': eligibility_result['corrected_interest_rate'],
            'tenure': tenure,
            'monthly_installment': round(eligibility_result['monthly_installment'], 2)
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_loan(request):
    """
    Create a new loan if eligible
    """
    serializer = LoanCreateSerializer(data=request.data)
    if serializer.is_valid():
        customer_id = serializer.validated_data['customer_id']
        loan_amount = serializer.validated_data['loan_amount']
        interest_rate = serializer.validated_data['interest_rate']
        tenure = serializer.validated_data['tenure']
        
        # Check eligibility first
        eligibility_result = check_loan_eligibility(
            customer_id, loan_amount, interest_rate, tenure
        )
        
        if not eligibility_result['eligible']:
            response_data = {
                'loan_id': None,
                'customer_id': customer_id,
                'loan_approved': False,
                'message': eligibility_result['message'],
                'monthly_installment': round(eligibility_result['monthly_installment'], 2)
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        # Create the loan
        try:
            customer = Customer.objects.get(customer_id=customer_id)
            
            # Calculate dates
            start_date = date.today()
            end_date = start_date + relativedelta(months=tenure)
            
            # Use corrected interest rate
            corrected_rate = eligibility_result['corrected_interest_rate']
            monthly_installment = eligibility_result['monthly_installment']
            
            loan = Loan.objects.create(
                customer=customer,
                loan_amount=loan_amount,
                tenure=tenure,
                interest_rate=Decimal(str(corrected_rate)),
                monthly_repayment=Decimal(str(monthly_installment)),
                start_date=start_date,
                end_date=end_date,
                emis_paid_on_time=0
            )
            
            # Update customer's current debt
            customer.current_debt = (customer.current_debt or 0) + loan_amount
            customer.save()
            
            response_data = {
                'loan_id': loan.loan_id,
                'customer_id': customer_id,
                'loan_approved': True,
                'message': 'Loan approved successfully',
                'monthly_installment': round(monthly_installment, 2)
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Customer.DoesNotExist:
            response_data = {
                'loan_id': None,
                'customer_id': customer_id,
                'loan_approved': False,
                'message': 'Customer not found',
                'monthly_installment': 0
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_loan(request, loan_id):
    """
    View details of a specific loan
    """
    loan = get_object_or_404(Loan, loan_id=loan_id)
    serializer = LoanDetailSerializer(loan)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_customer_loans(request, customer_id):
    """
    View all loans for a specific customer
    """
    customer = get_object_or_404(Customer, customer_id=customer_id)
    loans = Loan.objects.filter(customer=customer)
    serializer = CustomerLoanSerializer(loans, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def api_root(request):
    """
    List all available API endpoints
    """
    return Response({
        'message': 'Welcome to the Credit Approval System API',
        'endpoints': {
            'register_customer': '/register/',
            'check_eligibility': '/check-eligibility/',
            'create_loan': '/create-loan/',
            'view_loan': '/view-loan/<loan_id>/',
            'view_customer_loans': '/view-loans/<customer_id>/',
        },
        'documentation': 'See README.md for detailed usage instructions'
    }, status=status.HTTP_200_OK)
