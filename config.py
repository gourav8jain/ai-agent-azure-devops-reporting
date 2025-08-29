import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Centralized configuration for Azure DevOps and email settings"""
    
    # Core Azure DevOps Configuration
    AZURE_DEVOPS_ORG = os.getenv('AZURE_DEVOPS_ORG', 'delhivery')
    AZURE_DEVOPS_PAT = os.getenv('AZURE_DEVOPS_PAT', '')
    
    # Email Configuration
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
        'date_range_days': 30,
        'include_completed_sprints': False,
        'filter_by_tags': ['HRMS - Payout'],
        'exclude_projects': [],
        'include_projects': ['NEWTON', 'Partner Management Tool']
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
    
    # Sprint Period Configuration
    SPRINT_PERIOD = {
        'start_date': '19-Aug-2025',
        'end_date': '01-Sep-2025',
        'format': '%d-%b-%Y'
    }
    
    # Project Configuration
    PROJECTS = {
        'NEWTON': {
            'name': 'NEWTON',
            'tags': ['HRMS - Payout'],
            'iteration_path': 'NEWTON\\NEWTON Q2 19-Aug-2025 - 01-Sep-2025'
        },
        'PMT': {
            'name': 'Partner Management Tool',
            'tags': [],
            'iteration_path': 'Partner Management Tool\\PMT Q2 19-Aug-2025 - 01-Sep-2025'
        }
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
            print("Please set these in your .env file")
            return False
        
        return True
    
    @classmethod
    def get_project_config(cls, project_name):
        """Get configuration for a specific project"""
        for key, config in cls.PROJECTS.items():
            if key in project_name or config['name'] in project_name:
                return config
        return None
    
    @classmethod
    def get_state_category(cls, state):
        """Get the abstracted category for a given state"""
        for category, states in cls.STATE_CATEGORIES.items():
            if state in states:
                return category
        return 'Other'
