@echo off
echo ========================================
echo Credit Approval System - Demo Setup
echo ========================================
echo.

echo Starting Django server in background...
start "Django Server" /MIN powershell -Command "cd '%~dp0'; python manage.py runserver"

echo Waiting for server to start...
timeout /t 5 /nobreak

echo.
echo ========================================
echo Running API Demo Script
echo ========================================
python demo_script.py

echo.
echo ========================================
echo Demo Complete!
echo ========================================
echo.
echo The Django server is still running in the background.
echo You can now:
echo 1. Access http://localhost:8000 in your browser
echo 2. Use Postman/curl to test individual endpoints
echo 3. Record your video demo
echo.
echo To stop the server, close the Django Server window.
echo.
pause
