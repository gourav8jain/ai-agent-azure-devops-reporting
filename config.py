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
    EMAIL_TO = os.getenv('EMAIL_TO', 'gourav.jain@iol.world')
    
    # Multiple Email Recipients (comma-separated)
    # Example: "user1@company.com,user2@company.com,user3@company.com"
    EMAIL_TO_MULTIPLE = os.getenv('EMAIL_TO_MULTIPLE', '')
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
                    'sprint_duration_weeks': 3,  # IOL Pay has 3-week sprints
                    'iteration_path': 'IOL_X\\Charlie Backend Team Backlog\\Iteration-29',  # Base path; last segment auto-updated when API unavailable
                    'iteration_display': 'Iteration-29 (Nov 4 - Nov 24)',  # Display with dates
                    # Fallback cadence (used only if Azure DevOps API is unavailable)
                    # Anchor: Iteration-29 starting Nov 4, 2024, 3-week cadence
                    'fallback_cadence': {
                        'anchor_start': '2024-11-04',
                        'anchor_number': 29,
                        'duration_weeks': 3,
                        'name_prefix': 'Iteration-'
                    }
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
                    'sprint_duration_weeks': 2,  # VCC has 2-week sprints
                    'iteration_path': 'VCCWallet\\Sprint 12',  # Base path; last segment auto-updated when API unavailable
                    'iteration_display': 'Sprint-12 (Oct 28 - Nov 10)',  # Display with dates
                    # Fallback cadence (used only if Azure DevOps API is unavailable)
                    # Anchor: Sprint 12 starting Oct 28, 2024, 2-week cadence
                    'fallback_cadence': {
                        'anchor_start': '2024-10-28',
                        'anchor_number': 12,
                        'duration_weeks': 2,
                        'name_prefix': 'Sprint '
                    }
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
    def get_current_sprint_period(cls, project_key=None):
        """Get the current sprint period for a specific project or all projects.
        
        If project_key is provided, returns sprint period for that project.
        If not provided, returns a default period (for backward compatibility).
        """
        if project_key:
            # Get project-specific sprint period
            return cls.get_project_sprint_period(project_key)
        
        # Default: Return earliest start and latest end across all projects
        # This is used for backward compatibility
        all_periods = []
        for org_key, org_config in cls.ORGANIZATIONS.items():
            for proj_key, proj_config in org_config['projects'].items():
                period = cls.get_project_sprint_period(proj_key)
                if period:
                    all_periods.append(period)
        
        # Filter out fallback periods that don't have dates
        periods_with_dates = [
            p for p in all_periods 
            if not p.get('fallback') and 'start_datetime' in p and 'end_datetime' in p
        ]
        
        if periods_with_dates:
            earliest_start = min(p['start_datetime'] for p in periods_with_dates)
            latest_end = max(p['end_datetime'] for p in periods_with_dates)
            
            start_date_str = earliest_start.strftime('%d-%b-%Y')
            end_date_str = latest_end.strftime('%d-%b-%Y')
            start_iso = earliest_start.strftime('%Y-%m-%dT00:00:00')
            end_iso = latest_end.strftime('%Y-%m-%dT23:59:59')
            
            return {
                'start_date': start_date_str,
                'end_date': end_date_str,
                'start_datetime': earliest_start,
                'end_datetime': latest_end,
                'start_iso': start_iso,
                'end_iso': end_iso
            }
        
        # If we didn't find any non-fallback periods with dates,
        # try any periods that at least have dates (including fallback-derived ones)
        any_with_dates = [
            p for p in all_periods
            if 'start_datetime' in p and 'end_datetime' in p
        ]
        if any_with_dates:
            earliest_start = min(p['start_datetime'] for p in any_with_dates)
            latest_end = max(p['end_datetime'] for p in any_with_dates)

            start_date_str = earliest_start.strftime('%d-%b-%Y')
            end_date_str = latest_end.strftime('%d-%b-%Y')
            start_iso = earliest_start.strftime('%Y-%m-%dT00:00:00')
            end_iso = latest_end.strftime('%Y-%m-%dT23:59:59')

            return {
                'start_date': start_date_str,
                'end_date': end_date_str,
                'start_datetime': earliest_start,
                'end_datetime': latest_end,
                'start_iso': start_iso,
                'end_iso': end_iso
            }

        # Fallback to old hardcoded dates
        sprint_start = datetime(2024, 10, 14)
        sprint_end = datetime(2024, 10, 27)
        
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
    
    @classmethod
    def get_project_sprint_period(cls, project_key):
        """Get sprint period for a specific project based on current iteration from Azure DevOps"""
        # Find project configuration
        project_config = None
        for org_key, org_config in cls.ORGANIZATIONS.items():
            if project_key in org_config['projects']:
                project_config = org_config['projects'][project_key]
                break
        
        if not project_config:
            return None
        
        # Try to fetch current iteration from Azure DevOps
        from get_sprint_count import get_current_iteration
        
        # Get organization and project details
        org_name = None
        for org_key, org_config in cls.ORGANIZATIONS.items():
            if project_key in org_config['projects']:
                org_name = org_config['name']
                break
        
        if not org_name:
            return None
        
        # Fetch current iteration
        iteration_info = get_current_iteration(org_name, project_key, project_config.get('team_name'))
        
        if iteration_info and iteration_info.get('start_date') and iteration_info.get('end_date'):
            # Use dates from Azure DevOps
            start_date = iteration_info['start_date']
            end_date = iteration_info['end_date']
            
            # Parse dates from Azure DevOps format (ISO 8601)
            if isinstance(start_date, str):
                # Handle both '2024-10-14T00:00:00Z' and '2024-10-14' formats
                try:
                    if 'T' in start_date:
                        start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                    else:
                        start_date = datetime.strptime(start_date, '%Y-%m-%d')
                except:
                    start_date = datetime.strptime(start_date.split('T')[0], '%Y-%m-%d')
                
                # Convert to datetime object if it's a date
                if hasattr(start_date, 'date'):
                    start_date = datetime.combine(start_date.date(), datetime.min.time())
            elif not isinstance(start_date, datetime):
                # If it's already a date object, convert to datetime
                start_date = datetime.combine(start_date, datetime.min.time())
            
            if isinstance(end_date, str):
                try:
                    if 'T' in end_date:
                        end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                    else:
                        end_date = datetime.strptime(end_date, '%Y-%m-%d')
                except:
                    end_date = datetime.strptime(end_date.split('T')[0], '%Y-%m-%d')
                
                if hasattr(end_date, 'date'):
                    end_date = datetime.combine(end_date.date(), datetime.min.time())
            elif not isinstance(end_date, datetime):
                end_date = datetime.combine(end_date, datetime.min.time())
            
            start_date_str = start_date.strftime('%d-%b-%Y')
            end_date_str = end_date.strftime('%d-%b-%Y')
            start_iso = start_date.strftime('%Y-%m-%dT00:00:00')
            end_iso = end_date.strftime('%Y-%m-%dT23:59:59')
            
            return {
                'start_date': start_date_str,
                'end_date': end_date_str,
                'start_datetime': start_date,
                'end_datetime': end_date,
                'start_iso': start_iso,
                'end_iso': end_iso,
                'iteration_path': iteration_info.get('path'),
                'iteration_name': iteration_info.get('name')
            }
        
        # Fallback: compute the sprint in which the current date lies, using cadence.
        # Use configured iteration_path only as a base template (replace last segment with current iteration).
        cadence = project_config.get('fallback_cadence')
        base_iteration_path = project_config.get('iteration_path')
        if cadence:
            try:
                anchor_start = datetime.strptime(cadence['anchor_start'], '%Y-%m-%d')
                duration_days = int(cadence['duration_weeks']) * 7
                name_prefix = cadence.get('name_prefix', '')
                anchor_number = int(cadence['anchor_number'])
                today = datetime.now()
                # Sprint in which current date lies: find n such that today is in [anchor + n*duration, anchor + (n+1)*duration - 1]
                delta_days = (today.date() - anchor_start.date()).days
                n = max(0, delta_days // duration_days)
                current_start = anchor_start + timedelta(days=n * duration_days)
                current_end = current_start + timedelta(days=duration_days - 1)
                current_number = anchor_number + n
                iteration_name = f"{name_prefix}{current_number}"
                # Build full iteration_path from base (e.g. IOL_X\...\Iteration-29 -> IOL_X\...\Iteration-32)
                iteration_path = None
                if base_iteration_path and '\\' in base_iteration_path:
                    parts = base_iteration_path.split('\\')
                    parts[-1] = iteration_name
                    iteration_path = '\\'.join(parts)
                return {
                    'start_date': current_start.strftime('%d-%b-%Y'),
                    'end_date': current_end.strftime('%d-%b-%Y'),
                    'start_datetime': current_start,
                    'end_datetime': current_end,
                    'start_iso': current_start.strftime('%Y-%m-%dT00:00:00'),
                    'end_iso': current_end.strftime('%Y-%m-%dT23:59:59'),
                    'iteration_path': iteration_path,
                    'iteration_name': iteration_name,
                    'fallback': True
                }
            except Exception as e:
                print(f"   ⚠️ Error computing sprint from cadence: {e}")
        # If no cadence or calculation failed, use configured path as-is
        if base_iteration_path:
            return {
                'iteration_path': base_iteration_path,
                'iteration_name': base_iteration_path.split('\\')[-1],
                'fallback': True
            }
        return None
    
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
    
    @classmethod
    def get_email_recipients(cls):
        """Get email recipients - either single or multiple"""
        if cls.EMAIL_TO_MULTIPLE and cls.EMAIL_TO_MULTIPLE.strip():
            # Multiple recipients (comma-separated)
            recipients = [email.strip() for email in cls.EMAIL_TO_MULTIPLE.split(',') if email.strip()]
            return recipients
        else:
            # Single recipient
            return [cls.EMAIL_TO] if cls.EMAIL_TO else []