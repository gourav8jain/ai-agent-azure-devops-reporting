import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import calendar

# Load .env file for local development (if it exists)
# GitHub Actions will use repository secrets instead
load_dotenv()

class Config:
    """Centralized configuration for Azure DevOps and email settings"""
    
    # Core Azure DevOps Configuration
    # Priority: GitHub Secrets > .env file > Default Values
    AZURE_DEVOPS_ORG = os.getenv('AZURE_DEVOPS_ORG', 'delhivery')
    AZURE_DEVOPS_PAT = os.getenv('AZURE_DEVOPS_PAT', '')
    
    # Email Configuration
    # Priority: GitHub Secrets > .env file > Default Values
    EMAIL_FROM = os.getenv('EMAIL_FROM', '')
    EMAIL_TO = os.getenv('EMAIL_TO', '')
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    
    # Sprint Discovery Configuration
    SPRINT_DISCOVERY = {
        'enabled': True,
        'auto_discover': True,
        'date_range_days': 33, # Adjusted to cover the 2-week period
        'include_completed_sprints': False,
        'filter_by_tags': ['HRMS - Payout'],
        'exclude_projects': [],
        'include_projects': ['NEWTON', 'Partner Management Tool']
    }

    # Sprint Period (Dynamic based on current date)
    @classmethod
    def get_current_sprint_period(cls):
        """Dynamically determine current sprint period based on current date"""
        today = datetime.now()
        
        # Sprint cycles typically run in 2-week periods
        # Assuming sprints start on Mondays and end on Fridays
        # We'll calculate the current sprint based on today's date
        
        # Get the start of the current week (Monday)
        days_since_monday = today.weekday()
        current_week_start = today - timedelta(days=days_since_monday)
        
        # Sprint periods are typically 2 weeks (14 days)
        # Calculate which sprint cycle we're in
        days_since_epoch = (current_week_start - datetime(2024, 1, 1)).days
        sprint_cycle = days_since_epoch // 14
        
        # Calculate sprint start and end dates
        sprint_start = datetime(2024, 1, 1) + timedelta(days=sprint_cycle * 14)
        sprint_end = sprint_start + timedelta(days=13)  # 2 weeks minus 1 day
        
        # Format dates for Azure DevOps
        start_date_str = sprint_start.strftime('%d-%b-%Y')
        end_date_str = sprint_end.strftime('%d-%b-%Y')
        
        return {
            'start_date': start_date_str,
            'end_date': end_date_str,
            'start_datetime': sprint_start,
            'end_datetime': sprint_end
        }
    
    # Sprint Period (Dynamic - will be set by get_current_sprint_period)
    SPRINT_PERIOD = None

    # Project Specific Configuration
    @classmethod
    def get_projects_config(cls):
        """Get project configuration with dynamic iteration paths"""
        sprint_period = cls.get_current_sprint_period()
        
        return {
            'NEWTON': {
                'tags': ['HRMS - Payout'],
                'iteration_path': f"NEWTON\\NEWTON Q2 {sprint_period['start_date']} - {sprint_period['end_date']}"
            },
            'Partner Management Tool': {
                'tags': [],
                'iteration_path': f"Partner Management Tool\\PMT Q2 {sprint_period['start_date']} - {sprint_period['end_date']}"
            }
        }
    
    PROJECTS = None  # Will be set dynamically

    # State Categorization Configuration
    STATE_CATEGORIES = {
        'To-Do': ['Open', 'TO DO', 'New', 'REQ-Review'],
        'In Progress': ['In Progress', 'Code Review'],
        'In QA': ['On-QA', 'Fixed'],
        'Release Pending': ['QA Reviewed', 'SIGNOFF'],
        'Released': ['DONE', 'Done', 'Closed', 'Resolved', 'Completed'],
        'Drop': ['Drop']
    }
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        required_vars = [
            'AZURE_DEVOPS_PAT',
            'EMAIL_FROM',
            'EMAIL_TO',
            'SMTP_USERNAME',
            'SMTP_PASSWORD'
        ]
        
        # Check if we're running in GitHub Actions
        is_github_actions = os.getenv('GITHUB_ACTIONS') == 'true'
        
        print(f"🔧 Configuration Validation:")
        print(f"   Environment: {'GitHub Actions' if is_github_actions else 'Local Development'}")
        print(f"   .env file loaded: {os.path.exists('.env')}")
        
        missing_vars = []
        for var in required_vars:
            value = getattr(cls, var)
            if not value or value.strip() == '':
                missing_vars.append(var)
                print(f"   ❌ {var}: Not set or empty")
            else:
                # Show first 10 characters for security
                display_value = f"{value[:10]}..." if len(value) > 10 else value
                print(f"   ✅ {var}: {display_value}")
        
        if missing_vars:
            print(f"\n⚠️ Missing required environment variables: {', '.join(missing_vars)}")
            
            if is_github_actions:
                print("\n🔧 GitHub Actions Configuration:")
                print("   The workflow is running in GitHub Actions but environment variables are missing.")
                print("   Please check your repository secrets:")
                print("   Go to: Settings → Secrets and variables → Actions")
                print("   Ensure these secrets are set:")
                for var in missing_vars:
                    print(f"     - {var}")
                print("\n   Note: Repository secrets are automatically available as environment variables")
                print("   in GitHub Actions workflows.")
            else:
                print("\n🔧 Local Development Configuration:")
                print("   1. Copy .env.example to .env:")
                print("      cp .env.example .env")
                print("   2. Edit .env with your actual credentials")
                print("   3. Or set environment variables:")
                print("      export EMAIL_FROM=your_email@gmail.com")
                print("      export EMAIL_TO=recipient@gmail.com")
                print("      # etc...")
            
            return False
        
        print(f"\n✅ Configuration validation passed!")
        return True
    
    @classmethod
    def get_project_config(cls, project_name):
        """Get configuration for a specific project"""
        projects_config = cls.get_projects_config()
        return projects_config.get(project_name)
    
    @classmethod
    def get_state_category(cls, state):
        """Get the abstracted category for a given state"""
        for category, states in cls.STATE_CATEGORIES.items():
            if state in states:
                return category
        return 'Other'
