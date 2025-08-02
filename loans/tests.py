from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from .models import Customer, Loan
from .utils import calculate_credit_score, calculate_monthly_installment


class CustomerModelTest(TestCase):
    def test_customer_creation(self):
        """Test customer model creation"""
        customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            age=30,
            phone_number="1234567890",
            monthly_salary=Decimal('50000'),
            approved_limit=Decimal('1800000')
        )
        self.assertEqual(customer.first_name, "John")
        self.assertEqual(customer.monthly_salary, Decimal('50000'))
        self.assertEqual(str(customer), "John Doe (ID: {})".format(customer.customer_id))


class LoanModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            age=30,
            phone_number="1234567890",
            monthly_salary=Decimal('50000'),
            approved_limit=Decimal('1800000')
        )

    def test_loan_creation(self):
        """Test loan model creation"""
        loan = Loan.objects.create(
            customer=self.customer,
            loan_amount=Decimal('100000'),
            tenure=12,
            interest_rate=Decimal('10.0'),
            monthly_repayment=Decimal('8791'),
            start_date='2023-01-01',
            end_date='2023-12-31',
            emis_paid_on_time=0
        )
        self.assertEqual(loan.customer, self.customer)
        self.assertEqual(loan.loan_amount, Decimal('100000'))
        self.assertEqual(loan.repayments_left, 12)


class CreditScoringTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            age=30,
            phone_number="1234567890",
            monthly_salary=Decimal('50000'),
            approved_limit=Decimal('1800000')
        )

    def test_new_customer_credit_score(self):
        """Test credit score for new customer with no loan history"""
        score = calculate_credit_score(self.customer.customer_id)
        self.assertEqual(score, 85)

    def test_monthly_installment_calculation(self):
        """Test EMI calculation with compound interest"""
        emi = calculate_monthly_installment(100000, 10.0, 12)
        self.assertAlmostEqual(emi, 8791.59, places=2)


class APITestCase(APITestCase):
    def test_customer_registration(self):
        """Test customer registration endpoint"""
        url = reverse('register_customer')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 30,
            'monthly_income': 50000,
            'phone_number': '1234567890'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'John Doe')
        self.assertEqual(float(response.data['approved_limit']), 1800000)

    def test_loan_eligibility_check(self):
        """Test loan eligibility endpoint"""
        # First create a customer
        customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            age=30,
            phone_number="1234567890",
            monthly_salary=Decimal('50000'),
            approved_limit=Decimal('1800000')
        )
        
        url = reverse('check_eligibility')
        data = {
            'customer_id': customer.customer_id,
            'loan_amount': 100000,
            'interest_rate': 8.0,
            'tenure': 12
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['customer_id'], customer.customer_id)
        self.assertTrue(response.data['approval'])

    def test_loan_creation(self):
        """Test loan creation endpoint"""
        # First create a customer
        customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            age=30,
            phone_number="1234567890",
            monthly_salary=Decimal('50000'),
            approved_limit=Decimal('1800000')
        )
        
        url = reverse('create_loan')
        data = {
            'customer_id': customer.customer_id,
            'loan_amount': 100000,
            'interest_rate': 8.0,
            'tenure': 12
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['loan_approved'])
        self.assertIsNotNone(response.data['loan_id'])

    def test_view_loan(self):
        """Test view loan endpoint"""
        # Create customer and loan
        customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            age=30,
            phone_number="1234567890",
            monthly_salary=Decimal('50000'),
            approved_limit=Decimal('1800000')
        )
        
        loan = Loan.objects.create(
            customer=customer,
            loan_amount=Decimal('100000'),
            tenure=12,
            interest_rate=Decimal('10.0'),
            monthly_repayment=Decimal('8791'),
            start_date='2023-01-01',
            end_date='2023-12-31',
            emis_paid_on_time=0
        )
        
        url = reverse('view_loan', kwargs={'loan_id': loan.loan_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['loan_id'], loan.loan_id)
        self.assertEqual(response.data['customer']['first_name'], 'John')

    def test_view_customer_loans(self):
        """Test view customer loans endpoint"""
        # Create customer and loan
        customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            age=30,
            phone_number="1234567890",
            monthly_salary=Decimal('50000'),
            approved_limit=Decimal('1800000')
        )
        
        Loan.objects.create(
            customer=customer,
            loan_amount=Decimal('100000'),
            tenure=12,
            interest_rate=Decimal('10.0'),
            monthly_repayment=Decimal('8791'),
            start_date='2023-01-01',
            end_date='2023-12-31',
            emis_paid_on_time=0
        )
        
        url = reverse('view_customer_loans', kwargs={'customer_id': customer.customer_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(float(response.data[0]['loan_amount']), 100000)
