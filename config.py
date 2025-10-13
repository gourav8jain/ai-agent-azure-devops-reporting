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
    
    # Personal Access Token for both organizations
    AZURE_DEVOPS_PAT = os.getenv('AZURE_DEVOPS_PAT', '')
    
    # Email Configuration
    # Priority: GitHub Secrets > .env file > Default Values
    EMAIL_FROM = os.getenv('EMAIL_FROM', 'gourav8jain@gmail.com')
    EMAIL_TO = os.getenv('EMAIL_TO', 'gourav8jain@gmail.com')
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', 'gourav8jain@gmail.com')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    
    # Multi-Organization Configuration
    ORGANIZATIONS = {
        'IWTX': {
            'name': 'IWTX',
            'projects': {
                'IOL_X': {
                    'project_name': 'IOL Pay',  # Display name: IOL Pay
                    'team_name': 'Charlie Backend Team',
                    'tags': [],
                    'iteration_path': 'IOL_X\\Charlie Backend Team Backlog\\Iteration-28',  # Current sprint: Iteration-28
                    'iteration_display': 'Iteration-28 (Oct 14 - Nov 3)'  # Display with dates
                }
            }
        },
        'IOLPulse': {
            'name': 'IOLPulse', 
            'projects': {
                'VCCWallet': {
                    'project_name': 'VCCWallet',
                    'team_name': 'VCCWallet Team',
                    'tags': [],
                    'iteration_path': 'VCCWallet\\Sprint 11',  # Current sprint: Sprint-11
                    'iteration_display': 'Sprint-11 (Oct 14 - Oct 27)'  # Display with dates
                }
            }
        }
    }
    
    # Sprint Discovery Configuration
    SPRINT_DISCOVERY = {
        'enabled': True,
        'auto_discover': True,
        'date_range_days': 33, # Adjusted to cover the 2-week period
        'include_completed_sprints': False,
        'filter_by_tags': [],  # Remove old filter
        'exclude_projects': [],
        'include_projects': ['IOL_X', 'VCCWallet']  # Updated to new projects
    }

    # Sprint Period (Current Sprint - October 2024)
    @classmethod
    def get_current_sprint_period(cls):
        """Get the current sprint period based on provided sprint schedules.
        
        Current Sprint (October 2024):
        - IOL Pay: Iteration-28 (Oct 14 - Nov 3, 3 weeks)
        - VCC: Sprint-11 (October 14 - October 27, 2 weeks)
        
        Using the overlapping period: Oct 14 - Oct 27 (2 weeks)
        """
        # Current sprint dates based on provided information
        sprint_start = datetime(2024, 10, 14)  # October 14, 2024
        sprint_end = datetime(2024, 10, 27)    # October 27, 2024

        start_date_str = sprint_start.strftime('%d-%b-%Y')
        end_date_str = sprint_end.strftime('%d-%b-%Y')
        start_iso = sprint_start.strftime('%Y-%m-%dT00:00:00')
        end_iso = sprint_end.strftime('%Y-%m-%dT23:59:59')

        return {
            'start_date': start_date_str,
            'end_date': end_date_str,
            'start_datetime': sprint_start,
            'end_datetime': sprint_end,
            'start_iso': start_iso,
            'end_iso': end_iso
        }
    
    # Sprint Period (Dynamic - will be set by get_current_sprint_period)
    SPRINT_PERIOD = None

    # Project Specific Configuration
    @classmethod
    def get_projects_config(cls):
        """Get project configuration with dynamic iteration paths"""
        sprint_period = cls.get_current_sprint_period()
        
        return {
            'IOL_X': {
                'tags': [],
                'iteration_path': None
            },
            'VCCWallet': {
                'tags': [],
                'iteration_path': None
            }
        }
    
    PROJECTS = None  # Will be set dynamically

    # State Categorization Configuration
    STATE_CATEGORIES = {
        'To Do': ['Open', 'TO DO', 'New', 'REQ-Review', 'To Do'],
        'In Progress': ['In Progress', 'Code Review', 'Active', 'In Development'],
        'Ready for QA': ['On-QA', 'Fixed', 'Ready for QA', 'QA Ready'],
        'QA in Progress': ['QA in Progress', 'QA Testing', 'In QA'],
        'Ready for Release': ['QA Reviewed', 'SIGNOFF', 'Ready for Release', 'Release Ready'],
        'Done': ['DONE', 'Done', 'Closed', 'Resolved', 'Completed', 'Released']
    }
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        required_vars = [
            'AZURE_DEVOPS_PAT',
            'EMAIL_FROM',
            'EMAIL_TO',
            'SMTP_USERNAME'
        ]
        
        # Optional for testing
        optional_vars = ['SMTP_PASSWORD']
        
        # Check if we're running in GitHub Actions
        is_github_actions = os.getenv('GITHUB_ACTIONS') == 'true'
        
        print(f"🔧 Configuration Validation:")
        print(f"   Environment: {'GitHub Actions' if is_github_actions else 'Local Development'}")
        print(f"   .env file loaded: {os.path.exists('.env')}")
        
        missing_vars = []
        
        # Check required variables
        for var in required_vars:
            value = getattr(cls, var)
            if not value or value.strip() == '':
                missing_vars.append(var)
                print(f"   ❌ {var}: Not set or empty")
            else:
                # Show first 10 characters for security
                display_value = f"{value[:10]}..." if len(value) > 10 else value
                print(f"   ✅ {var}: {display_value}")
        
        # Check optional variables
        for var in optional_vars:
            value = getattr(cls, var)
            if not value or value.strip() == '':
                print(f"   ⚠️ {var}: Not set or empty (optional)")
            else:
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