import os
from dotenv import load_dotenv

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

    # Sprint Period (Manual Override for specific sprint)
    SPRINT_PERIOD = {
        'start_date': '19-Aug-2025',
        'end_date': '01-Sep-2025'
    }

    # Project Specific Configuration
    PROJECTS = {
        'NEWTON': {
            'tags': ['HRMS - Payout'],
            'iteration_path': 'NEWTON\\NEWTON Q2 19-Aug-2025 - 01-Sep-2025'
        },
        'Partner Management Tool': {
            'tags': [],
            'iteration_path': 'Partner Management Tool\\PMT Q2 19-Aug-2025 - 01-Sep-2025'
        }
    }

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
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️ Missing required environment variables: {', '.join(missing_vars)}")
            print("\n🔧 Configuration Options:")
            print("   1. Local Development (.env file):")
            print("      cp .env.example .env")
            print("      # Edit .env with your credentials")
            print("\n   2. GitHub Actions (Repository Secrets):")
            print("      Go to: Settings → Secrets and variables → Actions")
            print("      Add these secrets:")
            for var in missing_vars:
                print(f"        - {var}")
            print("\n   3. Environment Variables:")
            print("      export EMAIL_FROM=your_email@gmail.com")
            print("      export EMAIL_TO=recipient@gmail.com")
            print("      # etc...")
            return False
        
        return True
    
    @classmethod
    def get_project_config(cls, project_name):
        """Get configuration for a specific project"""
        return cls.PROJECTS.get(project_name)
    
    @classmethod
    def get_state_category(cls, state):
        """Get the abstracted category for a given state"""
        for category, states in cls.STATE_CATEGORIES.items():
            if state in states:
                return category
        return 'Other'
