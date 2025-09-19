#!/bin/bash

echo "🌊 Agro-Ocean SIH Streamlit Application Setup"
echo "============================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✅ pip found: $(pip3 --version)"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Run the application
echo "🚀 Starting Streamlit application..."
echo "📊 The application will open at: http://localhost:8501"
echo "🔑 Demo accounts:"
echo "   - Researcher: researcher@agro-ocean.com / password123"
echo "   - Analyst: analyst@agro-ocean.com / password123"
echo "   - Authority: authority@agro-ocean.com / password123"
echo "   - Fleet Manager: fleet@agro-ocean.com / password123"
echo ""
echo "Press Ctrl+C to stop the application"
echo "============================================="

streamlit run app.py