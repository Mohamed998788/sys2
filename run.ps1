# School Management System - Admin App Runner
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   School Management System - Admin" -ForegroundColor Cyan  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python is not installed or not in PATH" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Streamlit
Write-Host "Checking Streamlit installation..." -ForegroundColor Yellow
try {
    $streamlitCheck = python -c "import streamlit; print('Streamlit version:', streamlit.__version__)" 2>&1
    Write-Host "✓ $streamlitCheck" -ForegroundColor Green
} catch {
    Write-Host "✗ Streamlit is not installed" -ForegroundColor Red
    Write-Host "Installing Streamlit..." -ForegroundColor Yellow
    pip install streamlit
}

# Check .env file
Write-Host "Checking environment configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "⚠ .env file not found" -ForegroundColor Yellow
    Write-Host "Please copy .env.example to .env and configure your API keys" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Do you want to continue anyway? (y/n)"
    if ($continue -ne "y") {
        Write-Host "Setup cancelled" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "✓ Environment file found" -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting Streamlit application..." -ForegroundColor Green
Write-Host "🌐 Open your browser and go to: http://localhost:8501" -ForegroundColor Cyan
Write-Host "⏹ Press Ctrl+C to stop the application" -ForegroundColor Yellow
Write-Host ""

# Start Streamlit
try {
    streamlit run main.py
} catch {
    Write-Host "Error starting application: $_" -ForegroundColor Red
} finally {
    Write-Host ""
    Write-Host "Application stopped" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
}