#!/bin/bash

echo "🚀 Azure DevOps Sprint Report - Current Sprint Only"
echo "=================================================="
echo ""
echo "📅 Current Sprint Configuration:"
echo "   IOL Pay: Iteration-28 (Oct 14 - Nov 3)"
echo "   VCC: Sprint-11 (Oct 14 - Oct 27)"
echo ""

# Check if AZURE_DEVOPS_PAT is set
if [ -z "$AZURE_DEVOPS_PAT" ]; then
    echo "❌ AZURE_DEVOPS_PAT environment variable is not set"
    echo ""
    echo "🔧 To run this automation, you need to:"
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
    exit 1
fi

echo "✅ AZURE_DEVOPS_PAT is configured"
echo "🚀 Running complete workflow..."
echo ""

# Run the complete workflow
python3 run_complete_workflow_updated.py

echo ""
echo "🎉 Automation completed!"
