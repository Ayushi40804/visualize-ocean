@echo off
echo 🌊 Agro-Ocean SIH Streamlit Application Setup
echo =============================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed. Please install pip.
    pause
    exit /b 1
)

echo ✅ pip found
pip --version

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully

REM Run the application
echo 🚀 Starting Streamlit application...
echo 📊 The application will open at: http://localhost:8501
echo 🔑 Demo accounts:
echo    - Researcher: researcher@agro-ocean.com / password123
echo    - Analyst: analyst@agro-ocean.com / password123
echo    - Authority: authority@agro-ocean.com / password123
echo    - Fleet Manager: fleet@agro-ocean.com / password123
echo.
echo Press Ctrl+C to stop the application
echo =============================================

streamlit run app.py