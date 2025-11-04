#!/usr/bin/env python3
"""
Complete Azure DevOps Workflow Script
Runs the entire process: Extract → Generate → Send → Auto-commit
"""

import subprocess
import sys
import os
from datetime import datetime

def run_command(command, description):
    """Run a shell command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} successful")
            if result.stdout.strip():
                # Print output line by line for better readability
                output_lines = result.stdout.strip().split('\n')
                for line in output_lines:
                    if line.strip():
                        print(f"   {line}")
            return True
        else:
            print(f"❌ {description} failed")
            if result.stdout.strip():
                # Print stdout even on failure (may contain useful info)
                output_lines = result.stdout.strip().split('\n')
                for line in output_lines:
                    if line.strip():
                        print(f"   {line}")
            if result.stderr.strip():
                # Print stderr
                error_lines = result.stderr.strip().split('\n')
                for line in error_lines:
                    if line.strip():
                        print(f"   ERROR: {line}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {str(e)}")
        return False

def run_complete_workflow():
    """Run the complete Azure DevOps workflow"""
    print("🚀 Azure DevOps Complete Workflow")
    print("=" * 50)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Extract sprint data
    print("📊 Step 1: Extracting Sprint Data")
    print("-" * 30)
    if not run_command("python3 get_sprint_count.py", "Extracting sprint data from Azure DevOps"):
        print("❌ Sprint data extraction failed")
        return False
    
    print()
    
    # Step 2: Generate HTML report
    print("🎨 Step 2: Generating HTML Report")
    print("-" * 30)
    if not run_command("python3 generate_html_report_compact.py", "Generating compact HTML report"):
        print("❌ HTML report generation failed")
        return False
    
    print()
    
    # Step 3: Send email report
    print("📧 Step 3: Sending Email Report")
    print("-" * 30)
    if not run_command("python3 send_email_direct.py", "Sending report via email"):
        print("❌ Email sending failed")
        return False
    
    print()
    
    # Step 4: Auto commit and push
    print("🤖 Step 4: Auto Commit and Push")
    print("-" * 30)
    if not run_command("python3 auto_commit_push.py", "Auto-committing and pushing changes"):
        print("❌ Auto commit and push failed")
        return False
    
    print()
    print("🎉 Complete workflow executed successfully!")
    print(f"📅 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return True

def main():
    """Main function"""
    success = run_complete_workflow()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
