#!/usr/bin/env python3
"""
Auto Commit and Push Script
Automatically commits and pushes changes after successful execution
Only commits essential source code and configuration files
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

def should_commit_file(file_path):
    """Determine if a file should be committed"""
    # Essential files to always commit
    essential_files = {
        'config.py',
        'get_sprint_count.py',
        'generate_html_report_compact.py',
        'send_email_direct.py',
        'auto_commit_push.py',
        'run_complete_workflow.py',
        'run_and_commit.sh',
        'requirements.txt',
        'README.md',
        'AUTO_COMMIT_GUIDE.md',
        '.gitignore',
        '.github/workflows/daily-report.yml'
    }
    
    # Files to never commit
    never_commit = {
        '.env',
        '.env.local',
        '.env.*.local',
        'venv/',
        '__pycache__/',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '*.log',
        '*.tmp',
        '*.temp'
    }
    
    # Check if it's an essential file
    if file_path in essential_files:
        return True
    
    # Check if it's a file to never commit
    for pattern in never_commit:
        if pattern in file_path:
            return False
    
    # Check if it's a generated file
    if any(pattern in file_path for pattern in ['sprint_count_', 'compact_sprint_report_', 'sprint_report_']):
        return False
    
    # Check if it's an email or temporary file
    if any(pattern in file_path for pattern in ['email_content_', 'gmail_', '*.eml', '*.txt']):
        return False
    
    # Default: commit if it's a source code file
    return file_path.endswith(('.py', '.md', '.yml', '.yaml', '.sh', '.txt', '.gitignore'))

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
    
    # Filter files to commit
    files_to_commit = []
    files_to_ignore = []
    
    for line in status.split('\n'):
        if line.strip():
            file_path = line[3:].strip()  # Remove status indicators
            if should_commit_file(file_path):
                files_to_commit.append(file_path)
            else:
                files_to_ignore.append(file_path)
    
    if files_to_ignore:
        print(f"📝 Ignoring generated/temporary files:")
        for file_path in files_to_ignore:
            print(f"   ❌ {file_path}")
    
    if not files_to_commit:
        print("✅ No essential files to commit")
        return True
    
    print(f"📝 Essential files to commit:")
    for file_path in files_to_commit:
        print(f"   ✅ {file_path}")
    
    # Get current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Add only essential files
    for file_path in files_to_commit:
        if not run_command(f"git add {file_path}", f"Adding {file_path}"):
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
    print(f"📁 Files committed: {len(files_to_commit)}")
    print(f"🚫 Files ignored: {len(files_to_ignore)}")
    return True

def main():
    """Main function"""
    success = auto_commit_push()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
