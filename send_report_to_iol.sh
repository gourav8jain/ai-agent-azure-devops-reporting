#!/bin/bash

echo "🚀 Azure DevOps Sprint Report - Sending to gourav.jain@iol.world"
echo "================================================================"
echo ""
echo "📅 Current Sprint Configuration:"
echo "   IOL Pay: Iteration-28 (Oct 14 - Nov 3)"
echo "   VCC: Sprint-11 (Oct 14 - Oct 27)"
echo ""
echo "📧 Email Configuration:"
echo "   From: gourav8jain@gmail.com"
echo "   To: gourav.jain@iol.world"
echo ""

# Check if AZURE_DEVOPS_PAT is set
if [ -z "$AZURE_DEVOPS_PAT" ]; then
    echo "❌ AZURE_DEVOPS_PAT environment variable is not set"
    echo ""
    echo "🔧 To send the report to gourav.jain@iol.world, you need to:"
    echo "   1. Get your Azure DevOps Personal Access Token"
    echo "   2. Set the environment variable:"
    echo "      export AZURE_DEVOPS_PAT='your_pat_here'"
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
    echo "📧 Once configured, the report will be sent to: gourav.jain@iol.world"
    echo ""
    exit 1
fi

echo "✅ AZURE_DEVOPS_PAT is configured"
echo "🚀 Running complete workflow to send report to gourav.jain@iol.world..."
echo ""

# Run the complete workflow
python3 run_complete_workflow_updated.py

echo ""
echo "🎉 Report sent to gourav.jain@iol.world!"
echo "📊 The report includes:"
echo "   - IOL Pay (Iteration-28) current sprint data"
echo "   - VCC (Sprint-11) current sprint data"
echo "   - Updated status categories: To Do, In Progress, Ready for QA, QA in Progress, Ready for Release, Done"
