#!/bin/bash

# Azure DevOps Workflow with Auto-Commit
# This script runs the complete workflow and automatically commits changes

echo "🚀 Azure DevOps Workflow with Auto-Commit"
echo "=========================================="
echo "📅 Started at: $(date)"
echo ""

# Step 1: Extract sprint data
echo "📊 Step 1: Extracting Sprint Data"
echo "----------------------------------"
python3 get_sprint_count.py
if [ $? -ne 0 ]; then
    echo "❌ Sprint data extraction failed"
    exit 1
fi
echo ""

# Step 2: Generate HTML report
echo "🎨 Step 2: Generating HTML Report"
echo "----------------------------------"
python3 generate_html_report_compact.py
if [ $? -ne 0 ]; then
    echo "❌ HTML report generation failed"
    exit 1
fi
echo ""

# Step 3: Send email report
echo "📧 Step 3: Sending Email Report"
echo "----------------------------------"
python3 send_email_direct.py
if [ $? -ne 0 ]; then
    echo "❌ Email sending failed"
    exit 1
fi
echo ""

# Step 4: Auto commit and push
echo "🤖 Step 4: Auto Commit and Push"
echo "----------------------------------"
python3 auto_commit_push.py
if [ $? -ne 0 ]; then
    echo "❌ Auto commit and push failed"
    exit 1
fi
echo ""

echo "🎉 Complete workflow executed successfully!"
echo "📅 Completed at: $(date)"
echo "✅ All changes have been automatically committed and pushed to GitHub!"
