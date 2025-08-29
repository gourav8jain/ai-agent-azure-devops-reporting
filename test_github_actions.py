#!/usr/bin/env python3
"""
GitHub Actions Test Script
Tests the configuration and environment variables for GitHub Actions
"""

import os
from config import Config

def test_github_actions_environment():
    """Test the GitHub Actions environment"""
    print("🧪 GitHub Actions Environment Test")
    print("=" * 40)
    
    # Check if we're running in GitHub Actions
    is_github_actions = os.getenv('GITHUB_ACTIONS') == 'true'
    print(f"🏗️ Running in GitHub Actions: {is_github_actions}")
    
    if is_github_actions:
        print("✅ GitHub Actions environment detected")
        print(f"📊 Repository: {os.getenv('GITHUB_REPOSITORY', 'Not set')}")
        print(f"🌿 Branch: {os.getenv('GITHUB_REF_NAME', 'Not set')}")
        print(f"🔄 Workflow: {os.getenv('GITHUB_WORKFLOW', 'Not set')}")
    else:
        print("💻 Running in local environment")
    
    print()
    
    # Test environment variables
    print("🔍 Environment Variables Test:")
    print("-" * 30)
    
    env_vars = [
        'AZURE_DEVOPS_ORG',
        'AZURE_DEVOPS_PAT',
        'EMAIL_FROM',
        'EMAIL_TO',
        'SMTP_USERNAME',
        'SMTP_PASSWORD'
    ]
    
    all_set = True
    for var in env_vars:
        value = os.getenv(var)
        if value:
            # Show first 10 characters for security
            display_value = f"{value[:10]}..." if len(value) > 10 else value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: Not set")
            all_set = False
    
    print()
    
    # Test configuration validation
    print("🔧 Configuration Validation Test:")
    print("-" * 30)
    
    try:
        config_result = Config.validate_config()
        if config_result:
            print("✅ Configuration validation passed")
        else:
            print("❌ Configuration validation failed")
            all_set = False
    except Exception as e:
        print(f"❌ Configuration validation error: {str(e)}")
        all_set = False
    
    print()
    
    # Test Azure DevOps connection
    print("🔗 Azure DevOps Connection Test:")
    print("-" * 30)
    
    try:
        org = os.getenv('AZURE_DEVOPS_ORG')
        pat = os.getenv('AZURE_DEVOPS_PAT')
        
        if org and pat:
            print(f"✅ Azure DevOps Org: {org}")
            print(f"✅ PAT Status: {pat[:10]}...")
            print("✅ Ready to connect to Azure DevOps")
        else:
            print("❌ Missing Azure DevOps credentials")
            all_set = False
    except Exception as e:
        print(f"❌ Azure DevOps test error: {str(e)}")
        all_set = False
    
    print()
    
    # Test email configuration
    print("📧 Email Configuration Test:")
    print("-" * 30)
    
    try:
        email_from = os.getenv('EMAIL_FROM')
        email_to = os.getenv('EMAIL_TO')
        smtp_user = os.getenv('SMTP_USERNAME')
        smtp_pass = os.getenv('SMTP_PASSWORD')
        
        if all([email_from, email_to, smtp_user, smtp_pass]):
            print(f"✅ From: {email_from}")
            print(f"✅ To: {email_to}")
            print(f"✅ SMTP User: {smtp_user}")
            print(f"✅ Password Status: {smtp_pass[:10]}...")
            print("✅ Ready to send emails")
        else:
            print("❌ Missing email credentials")
            all_set = False
    except Exception as e:
        print(f"❌ Email test error: {str(e)}")
        all_set = False
    
    print()
    
    # Final result
    print("🎯 Final Test Result:")
    print("=" * 40)
    
    if all_set:
        print("✅ All tests passed! Ready for GitHub Actions!")
        print("🚀 The workflow should run successfully")
    else:
        print("❌ Some tests failed! Check the configuration")
        print("🔧 Ensure all required secrets are set in GitHub")
    
    return all_set

def main():
    """Main function"""
    success = test_github_actions_environment()
    exit(0 if success else 1)

if __name__ == "__main__":
    main()
