# HealthCheck AI Startup Script

Write-Host "Starting HealthCheck AI Backend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; py -m uvicorn main:app --reload --port 8001"

Write-Host "Starting HealthCheck AI Frontend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; python -m http.server 3000"

Write-Host "App is running!" -ForegroundColor Green
Write-Host "Backend API: http://localhost:8001"
Write-Host "Frontend: http://localhost:3000"

Start-Process "http://localhost:3000"
