from django.core.management.base import BaseCommand
from loans.tasks import ingest_customer_data, ingest_loan_data, update_customer_current_debt
import os


class Command(BaseCommand):
    help = 'Ingest customer and loan data from Excel files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--customer-file',
            type=str,
            help='Path to customer data Excel file',
            default='data/customer_data.xlsx'
        )
        parser.add_argument(
            '--loan-file',
            type=str,
            help='Path to loan data Excel file',
            default='data/loan_data.xlsx'
        )
        parser.add_argument(
            '--async',
            action='store_true',
            help='Run tasks asynchronously using Celery',
        )

    def handle(self, *args, **options):
        customer_file = options['customer_file']
        loan_file = options['loan_file']
        run_async = options['async']

        # Check if files exist
        if not os.path.exists(customer_file):
            self.stdout.write(
                self.style.ERROR(f'Customer file not found: {customer_file}')
            )
            return

        if not os.path.exists(loan_file):
            self.stdout.write(
                self.style.ERROR(f'Loan file not found: {loan_file}')
            )
            return

        if run_async:
            # Run tasks asynchronously
            self.stdout.write('Starting asynchronous data ingestion...')
            
            # Start customer data ingestion
            customer_task = ingest_customer_data.delay(customer_file)
            self.stdout.write(f'Customer data ingestion task started: {customer_task.id}')
            
            # Start loan data ingestion (should run after customer data)
            loan_task = ingest_loan_data.delay(loan_file)
            self.stdout.write(f'Loan data ingestion task started: {loan_task.id}')
            
            # Start current debt update
            debt_task = update_customer_current_debt.delay()
            self.stdout.write(f'Current debt update task started: {debt_task.id}')
            
        else:
            # Run tasks synchronously
            self.stdout.write('Starting synchronous data ingestion...')
            
            # Ingest customer data
            self.stdout.write('Ingesting customer data...')
            customer_result = ingest_customer_data(customer_file)
            self.stdout.write(self.style.SUCCESS(customer_result))
            
            # Ingest loan data
            self.stdout.write('Ingesting loan data...')
            loan_result = ingest_loan_data(loan_file)
            self.stdout.write(self.style.SUCCESS(loan_result))
            
            # Update current debt
            self.stdout.write('Updating current debt...')
            debt_result = update_customer_current_debt()
            self.stdout.write(self.style.SUCCESS(debt_result))
            
            self.stdout.write(
                self.style.SUCCESS('Data ingestion completed successfully!')
            )
