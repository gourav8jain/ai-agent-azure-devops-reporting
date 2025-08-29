#!/usr/bin/env python3
"""
GitHub Actions Workflow Verification Script
Verifies that the workflow file is properly structured
"""

import yaml
import os

def verify_workflow():
    """Verify the GitHub Actions workflow structure"""
    print("🔍 GitHub Actions Workflow Verification")
    print("=" * 50)
    
    workflow_file = ".github/workflows/daily-report.yml"
    
    if not os.path.exists(workflow_file):
        print("❌ Workflow file not found!")
        return False
    
    try:
        with open(workflow_file, 'r') as f:
            workflow = yaml.safe_load(f)
        
        print("✅ Workflow file loaded successfully")
        
        # Check job structure
        if 'jobs' not in workflow:
            print("❌ No jobs defined in workflow")
            return False
        
        job_name = 'generate-and-send-report'
        if job_name not in workflow['jobs']:
            print(f"❌ Job '{job_name}' not found")
            return False
        
        job = workflow['jobs'][job_name]
        
        # Check environment variables at job level
        if 'env' not in job:
            print("❌ No environment variables defined at job level")
            return False
        
        required_env_vars = [
            'AZURE_DEVOPS_ORG',
            'AZURE_DEVOPS_PAT', 
            'EMAIL_FROM',
            'EMAIL_TO',
            'SMTP_USERNAME',
            'SMTP_PASSWORD'
        ]
        
        job_env = job['env']
        missing_env = []
        
        for var in required_env_vars:
            if var not in job_env:
                missing_env.append(var)
        
        if missing_env:
            print(f"❌ Missing environment variables at job level: {', '.join(missing_env)}")
            return False
        
        print("✅ All required environment variables defined at job level")
        
        # Check steps
        if 'steps' not in job:
            print("❌ No steps defined in job")
            return False
        
        steps = job['steps']
        step_names = [step['name'] for step in steps]
        
        required_steps = [
            'Checkout repository',
            'Set up Python',
            'Install dependencies',
            'Debug Environment',
            'Debug Environment Variables for Validation',
            'Validate Configuration',
            'Generate Sprint Report',
            'Generate HTML Report',
            'Send Email Report',
            'Upload Report Artifacts',
            'Success Notification'
        ]
        
        missing_steps = []
        for step in required_steps:
            if step not in step_names:
                missing_steps.append(step)
        
        if missing_steps:
            print(f"❌ Missing required steps: {', '.join(missing_steps)}")
            return False
        
        print("✅ All required steps defined")
        
        # Check that no steps have individual env sections
        steps_with_env = []
        for step in steps:
            if 'env' in step:
                steps_with_env.append(step['name'])
        
        if steps_with_env:
            print(f"⚠️ Steps with individual env sections (should be at job level): {', '.join(steps_with_env)}")
            print("   This might cause environment variable access issues")
        else:
            print("✅ No steps with individual env sections (good!)")
        
        print("\n🎯 Workflow Structure Summary:")
        print(f"   - Environment variables: {len(job_env)}/6 at job level")
        print(f"   - Steps: {len(steps)}/11 defined")
        print(f"   - Job-level env: ✅ Present")
        print(f"   - Step-level env: {'⚠️ Present' if steps_with_env else '✅ None'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying workflow: {str(e)}")
        return False

def main():
    """Main function"""
    success = verify_workflow()
    if success:
        print("\n✅ Workflow verification passed!")
        print("🚀 The workflow should now work properly in GitHub Actions")
    else:
        print("\n❌ Workflow verification failed!")
        print("🔧 Please check the workflow file structure")
    
    return success

if __name__ == "__main__":
    main()
