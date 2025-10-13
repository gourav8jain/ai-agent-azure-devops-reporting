#!/bin/bash

echo "🚀 Azure DevOps Sprint Report - Multiple Email Recipients"
echo "========================================================="
echo ""
echo "📅 Current Sprint Configuration:"
echo "   IOL Pay: Iteration-28 (Oct 14 - Nov 3)"
echo "   VCC: Sprint-11 (Oct 14 - Oct 27)"
echo ""

# Check if AZURE_DEVOPS_PAT is set
if [ -z "$AZURE_DEVOPS_PAT" ]; then
    echo "❌ AZURE_DEVOPS_PAT environment variable is not set"
    echo ""
    echo "🔧 To send the report to multiple emails, you need to:"
    echo "   1. Get your Azure DevOps Personal Access Token"
    echo "   2. Set the environment variables:"
    echo "      export AZURE_DEVOPS_PAT='your_pat_here'"
    echo "      export EMAIL_TO_MULTIPLE='email1@company.com,email2@company.com,email3@company.com'"
    echo "   3. Then run this script again"
    echo ""
    echo "🔑 How to get Azure DevOps PAT:"
    echo "   1. Go to: https://dev.azure.com"
    echo "   2. Click your profile → Personal Access Tokens"
    echo "   3. Create new token with permissions:"
    echo "      - Work Items: Read"
    echo "      - Project and Team: Read"
    echo "      - Sprints: Read"
    echo ""
    echo "📧 Multiple Email Configuration:"
    echo "   Set EMAIL_TO_MULTIPLE with comma-separated emails:"
    echo "   export EMAIL_TO_MULTIPLE='gourav.jain@iol.world,manager@company.com,team@company.com'"
    echo ""
    exit 1
fi

# Check if EMAIL_TO_MULTIPLE is set
if [ -z "$EMAIL_TO_MULTIPLE" ]; then
    echo "⚠️ EMAIL_TO_MULTIPLE not set, using single recipient: gourav.jain@iol.world"
    echo ""
    echo "💡 To send to multiple emails, set:"
    echo "   export EMAIL_TO_MULTIPLE='email1@company.com,email2@company.com,email3@company.com'"
    echo ""
else
    echo "✅ EMAIL_TO_MULTIPLE is configured"
    echo "📧 Sending to: $EMAIL_TO_MULTIPLE"
    echo ""
fi

echo "✅ AZURE_DEVOPS_PAT is configured"
echo "🚀 Running complete workflow to send report to multiple recipients..."
echo ""

# Run the complete workflow
python3 run_complete_workflow_updated.py

echo ""
echo "🎉 Report sent to all recipients!"
echo "📊 The report includes:"
echo "   - IOL Pay (Iteration-28) current sprint data"
echo "   - VCC (Sprint-11) current sprint data"
echo "   - Updated status categories: To Do, In Progress, Ready for QA, QA in Progress, Ready for Release, Done"
