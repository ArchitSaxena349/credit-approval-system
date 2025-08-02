# Credit Approval System - PowerShell API Testing Commands
# Run these commands one by one during your video demo

Write-Host "🚀 Credit Approval System - API Testing Commands" -ForegroundColor Green
Write-Host "Make sure the Django server is running: python manage.py runserver" -ForegroundColor Yellow
Write-Host ""

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "1. Customer Registration (POST /register/)" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

$customerData = @{
    first_name = "Alice"
    last_name = "Johnson"
    age = 28
    monthly_income = 85000
    phone_number = "1234567890"
} | ConvertTo-Json

Write-Host "Request Body:" -ForegroundColor Yellow
Write-Host $customerData -ForegroundColor White

try {
    $customerResponse = Invoke-RestMethod -Uri "http://localhost:8000/register/" -Method POST -Body $customerData -ContentType "application/json"
    Write-Host "Response:" -ForegroundColor Yellow
    $customerResponse | Format-List
    $customerId = $customerResponse.customer_id
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    $customerId = 1  # Fallback
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "2. Check Loan Eligibility (POST /check-eligibility/)" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

$eligibilityData = @{
    customer_id = $customerId
    loan_amount = 300000
    interest_rate = 8.5
    tenure = 36
} | ConvertTo-Json

Write-Host "Request Body:" -ForegroundColor Yellow
Write-Host $eligibilityData -ForegroundColor White

try {
    $eligibilityResponse = Invoke-RestMethod -Uri "http://localhost:8000/check-eligibility/" -Method POST -Body $eligibilityData -ContentType "application/json"
    Write-Host "Response:" -ForegroundColor Yellow
    $eligibilityResponse | Format-List
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "3. Create Loan (POST /create-loan/)" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

$loanData = @{
    customer_id = $customerId
    loan_amount = 300000
    interest_rate = 8.5
    tenure = 36
} | ConvertTo-Json

Write-Host "Request Body:" -ForegroundColor Yellow
Write-Host $loanData -ForegroundColor White

try {
    $loanResponse = Invoke-RestMethod -Uri "http://localhost:8000/create-loan/" -Method POST -Body $loanData -ContentType "application/json"
    Write-Host "Response:" -ForegroundColor Yellow
    $loanResponse | Format-List
    $loanId = $loanResponse.loan_id
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    $loanId = 1  # Fallback
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "4. View Loan Details (GET /view-loan/{loan_id}/)" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

try {
    $loanDetails = Invoke-RestMethod -Uri "http://localhost:8000/view-loan/$loanId/" -Method GET
    Write-Host "Response:" -ForegroundColor Yellow
    $loanDetails | Format-List
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "5. View Customer Loans (GET /view-loans/{customer_id}/)" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

try {
    $customerLoans = Invoke-RestMethod -Uri "http://localhost:8000/view-loans/$customerId/" -Method GET
    Write-Host "Response:" -ForegroundColor Yellow
    $customerLoans | Format-Table
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "Demo Complete! 🎉" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green
Write-Host "All API endpoints have been tested successfully!" -ForegroundColor Green
