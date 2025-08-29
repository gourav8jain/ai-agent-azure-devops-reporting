#!/bin/bash

# Azure DevOps AI Agent - Quick Start Script
# This script helps you get started quickly with the Azure DevOps reporting project

echo "🚀 Azure DevOps AI Agent - Quick Start"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Dependencies installed"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating one from template..."
    cp env.example .env
    echo "✅ .env file created from template"
    echo ""
    echo "📝 Please edit .env file with your actual credentials:"
    echo "   - Azure DevOps Personal Access Token"
    echo "   - Gmail credentials (with App Password)"
    echo ""
    echo "💡 For Gmail, you need to:"
    echo "   1. Enable 2-Step Verification"
    echo "   2. Generate an App Password at: https://myaccount.google.com/apppasswords"
    echo ""
    echo "🔐 After updating .env, run this script again to continue."
    exit 0
else
    echo "✅ .env file found"
fi

# Validate configuration
echo "🔍 Validating configuration..."
python3 -c "
from config import Config
if Config.validate_config():
    print('✅ Configuration is valid')
else:
    print('❌ Configuration validation failed')
    print('Please check your .env file')
    exit(1)
"

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Configuration validation failed. Please check your .env file."
    exit 1
fi

echo ""
echo "🎯 Configuration is valid! Ready to run."
echo ""

# Show available commands
echo "📋 Available Commands:"
echo "======================"
echo ""
echo "1. Extract Sprint Data:"
echo "   python3 get_sprint_count.py"
echo ""
echo "2. Generate HTML Report:"
echo "   python3 generate_html_report.py"
echo ""
echo "3. Send Email Report:"
echo "   python3 send_email_direct.py"
echo ""
echo "4. Full Workflow (Extract → Report → Email):"
echo "   python3 get_sprint_count.py && python3 generate_html_report.py && python3 send_email_direct.py"
echo ""

# Ask if user wants to run the full workflow
read -p "🤔 Would you like to run the full workflow now? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Running full workflow..."
    echo ""
    
    echo "📊 Step 1: Extracting sprint data..."
    python3 get_sprint_count.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "🎨 Step 2: Generating HTML report..."
        python3 generate_html_report.py
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "📧 Step 3: Sending email report..."
            python3 send_email_direct.py
            
            if [ $? -eq 0 ]; then
                echo ""
                echo "🎉 Workflow completed successfully!"
                echo "📧 Check your email for the report"
            else
                echo ""
                echo "❌ Email sending failed. Check the logs above."
            fi
        else
            echo ""
            echo "❌ HTML report generation failed. Check the logs above."
        fi
    else
        echo ""
        echo "❌ Sprint data extraction failed. Check the logs above."
    fi
else
    echo "ℹ️  You can run the commands manually when ready."
fi

echo ""
echo "📚 For more information, check the README.md file"
echo "🔧 For configuration help, check the env.example file"
echo ""
echo "Happy reporting! 🎯"
