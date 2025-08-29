#!/usr/bin/env python3
"""
Auto Commit and Push Script
Automatically commits and pushes changes after successful execution
"""

import subprocess
import os
import sys
from datetime import datetime

def run_command(command, description):
    """Run a shell command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} successful")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {str(e)}")
        return False

def get_git_status():
    """Get current git status"""
    try:
        result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        return ""
    except:
        return ""

def auto_commit_push():
    """Automatically commit and push changes"""
    print("🚀 Auto Commit and Push Script")
    print("=" * 40)
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("❌ Not in a git repository")
        return False
    
    # Get current git status
    status = get_git_status()
    if not status:
        print("✅ No changes to commit")
        return True
    
    print(f"📝 Changes detected:")
    for line in status.split('\n'):
        if line.strip():
            print(f"   {line}")
    
    # Get current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Add all changes
    if not run_command("git add .", "Adding all changes"):
        return False
    
    # Commit changes
    commit_message = f"🤖 Auto-commit: {timestamp} - Azure DevOps report execution"
    if not run_command(f'git commit -m "{commit_message}"', "Committing changes"):
        return False
    
    # Push changes
    if not run_command("git push origin main", "Pushing to remote"):
        return False
    
    print(f"\n🎉 Auto commit and push completed successfully!")
    print(f"📅 Timestamp: {timestamp}")
    return True

def main():
    """Main function"""
    success = auto_commit_push()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
