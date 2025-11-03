import requests
import json
import base64
from datetime import datetime
from config import Config

def get_current_iteration(organization, project, team_name=None):
    """Fetch the current iteration/sprint from Azure DevOps for a project"""
    
    if not Config.AZURE_DEVOPS_PAT:
        return None
    
    # Encode PAT for Basic Auth
    credentials = base64.b64encode(f":{Config.AZURE_DEVOPS_PAT}".encode()).decode()
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/json'
    }
    
    try:
        # First, get teams for the project
        teams_url = f"https://dev.azure.com/{organization}/{project}/_apis/teams?api-version=7.0"
        response = requests.get(teams_url, headers=headers)
        response.raise_for_status()
        teams_data = response.json()
        teams = teams_data.get('value', [])
        
        # Find the team by name if provided
        target_team = None
        if team_name:
            for team in teams:
                if team.get('name') == team_name:
                    target_team = team
                    break
        
        # Use first team if no specific team found
        if not target_team and teams:
            target_team = teams[0]
        
        if not target_team:
            print(f"   ⚠️ No team found for project {project}")
            return None
        
        team_id = target_team.get('id')
        
        # Get iterations for the team
        iterations_url = f"https://dev.azure.com/{organization}/{project}/{team_id}/_apis/work/teamsettings/iterations?api-version=7.0&$timeframe=current"
        response = requests.get(iterations_url, headers=headers)
        response.raise_for_status()
        iterations_data = response.json()
        iterations = iterations_data.get('value', [])
        
        # Find current iteration
        today = datetime.now().date()
        current_iteration = None
        
        for iteration in iterations:
            attrs = iteration.get('attributes', {})
            start_date = attrs.get('startDate')
            end_date = attrs.get('finishDate')
            
            if start_date and end_date:
                # Parse dates
                if isinstance(start_date, str):
                    start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00')).date()
                if isinstance(end_date, str):
                    end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00')).date()
                
                # Check if today is within this iteration
                if start_date <= today <= end_date:
                    current_iteration = {
                        'id': iteration.get('id'),
                        'name': iteration.get('name'),
                        'path': iteration.get('path'),
                        'start_date': attrs.get('startDate'),
                        'end_date': attrs.get('finishDate')
                    }
                    break
        
        # If no current iteration found, try to get the most recent future iteration
        if not current_iteration:
            for iteration in sorted(iterations, key=lambda x: x.get('attributes', {}).get('startDate', '')):
                attrs = iteration.get('attributes', {})
                start_date = attrs.get('startDate')
                
                if start_date:
                    if isinstance(start_date, str):
                        start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00')).date()
                    
                    if start_date >= today:
                        current_iteration = {
                            'id': iteration.get('id'),
                            'name': iteration.get('name'),
                            'path': iteration.get('path'),
                            'start_date': attrs.get('startDate'),
                            'end_date': attrs.get('finishDate')
                        }
                        break
        
        # If still no iteration, get the first iteration available
        if not current_iteration and iterations:
            iteration = iterations[0]
            attrs = iteration.get('attributes', {})
            current_iteration = {
                'id': iteration.get('id'),
                'name': iteration.get('name'),
                'path': iteration.get('path'),
                'start_date': attrs.get('startDate'),
                'end_date': attrs.get('finishDate')
            }
        
        if current_iteration:
            print(f"   ✅ Found current iteration: {current_iteration['name']} ({current_iteration.get('start_date')} to {current_iteration.get('end_date')})")
        
        return current_iteration
        
    except requests.exceptions.RequestException as e:
        print(f"   ⚠️ Error fetching iteration from Azure DevOps: {str(e)}")
        return None
    except Exception as e:
        print(f"   ⚠️ Unexpected error fetching iteration: {str(e)}")
        return None

def get_work_item_count(organization, project, tags=None, sprint_start=None, sprint_end=None, iteration_path=None):
    """Get work item count for a specific project and sprint period"""
    
    if not Config.AZURE_DEVOPS_PAT:
        print("❌ Azure DevOps PAT not configured")
        return None
    
    # Encode PAT for Basic Auth
    credentials = base64.b64encode(f":{Config.AZURE_DEVOPS_PAT}".encode()).decode()
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/json'
    }
    
    print(f"\n🔍 Querying {organization}/{project} project...")
    
    wiql_query = {
        'query': f"""
        SELECT [System.Id]
        FROM WorkItems 
        WHERE [System.TeamProject] = @project
        """
    }

    # Use iteration path filtering if available, otherwise use date range filtering
    if iteration_path:
        wiql_query["query"] += f"""
        AND [System.IterationPath] = '{iteration_path}'
        """
        print(f"   📋 Iteration path filtering: {iteration_path}")
    else:
        # Add date range filtering as fallback
        date_start = sprint_start.split('T', 1)[0]
        date_end = sprint_end.split('T', 1)[0]
        wiql_query["query"] += f"""
        AND [System.ChangedDate] >= '{date_start}'
        AND [System.ChangedDate] <= '{date_end}'
        """
        print(f"   📅 Date filtering: {date_start} to {date_end}")

    # Add tag filtering if specified
    if tags:
        tag_conditions = []
        for tag in tags:
            tag_conditions.append(f"[System.Tags] CONTAINS WORDS '{tag}'")

        if tag_conditions:
            wiql_query["query"] += f" AND ({' OR '.join(tag_conditions)})"
            print(f"   🏷️ Filtering by tags: {', '.join(tags)}")
    else:
        print(f"   ℹ️ No tags specified for filtering")

    # Execute WIQL query
    wiql_url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=7.0"
    
    try:
        response = requests.post(wiql_url, headers=headers, json=wiql_query)
        response.raise_for_status()
        
        wiql_result = response.json()
        work_item_ids = [item['id'] for item in wiql_result.get('workItems', [])]
        
        print(f"   📊 Found {len(work_item_ids)} work items")
        
        if not work_item_ids:
            return {'total_items': 0, 'engineer_metrics': {}}
        
        # Get detailed work item information
        return get_engineer_metrics(organization, project, work_item_ids, headers)
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error querying work items: {str(e)}")
        return None

def get_engineer_metrics(organization, project, work_item_ids, headers):
    """Get engineer-wise metrics for work items"""
    
    # Get work item details in batches
    batch_size = 200
    all_work_items = []
    
    for i in range(0, len(work_item_ids), batch_size):
        batch_ids = work_item_ids[i:i + batch_size]
        ids_param = ','.join(map(str, batch_ids))
        
        work_items_url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems?ids={ids_param}&$fields=System.Id,System.AssignedTo,System.State,System.Tags,System.Title&api-version=7.0"
        
        try:
            response = requests.get(work_items_url, headers=headers)
            response.raise_for_status()
            
            batch_result = response.json()
            all_work_items.extend(batch_result.get('value', []))
            
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error getting work item details: {str(e)}")
            continue
    
    # Process work items to get engineer metrics
    engineer_metrics = {}
    total_items = len(all_work_items)
    
    for work_item in all_work_items:
        fields = work_item.get('fields', {})
        assigned_to = fields.get('System.AssignedTo', {})
        state = fields.get('System.State', 'Unknown')
        tags = fields.get('System.Tags', '')
        title = fields.get('System.Title', 'Untitled Task')
        
        # Get assignee name
        if assigned_to and 'displayName' in assigned_to:
            assignee = assigned_to['displayName']
        else:
            assignee = 'Unassigned'
        
        # Initialize engineer metrics if not exists
        if assignee not in engineer_metrics:
            engineer_metrics[assignee] = {
                'total_items': 0,
                'states': {},
                'tasks': []
            }
        
        # Update metrics
        engineer_metrics[assignee]['total_items'] += 1
        engineer_metrics[assignee]['states'][state] = engineer_metrics[assignee]['states'].get(state, 0) + 1
        
        # Store task details
        task_info = {
            'title': title,
            'state': state,
            'tags': tags
        }
        engineer_metrics[assignee]['tasks'].append(task_info)
        
        # Store tags for verification
        if 'tags' not in engineer_metrics[assignee]:
            engineer_metrics[assignee]['tags'] = []
        engineer_metrics[assignee]['tags'].append(tags)
    
    return {
        'total_items': total_items,
        'engineer_metrics': engineer_metrics
    }

def main():
    """Main function to get sprint counts"""
    print("🚀 Azure DevOps Sprint Count Extractor")
    print("=" * 50)
    
    # Validate configuration
    if not Config.validate_config():
        print("❌ Configuration validation failed")
        return
    
    print(f"📅 Sprint calculated based on current date: {datetime.now().strftime('%d-%b-%Y')}")
    
    # Get counts for each organization and project
    all_results = {}
    
    for org_key, org_config in Config.ORGANIZATIONS.items():
        org_name = org_config['name']
        print(f"\n🏢 Processing organization: {org_name}")
        
        for project_key, project_config in org_config['projects'].items():
            project_name = project_key
            tags = project_config['tags']
            
            print(f"\n   📋 Processing project: {project_name}")
            
            # Get project-specific sprint period
            sprint_period = Config.get_current_sprint_period(project_key)
            
            if sprint_period:
                sprint_start_iso = sprint_period.get('start_iso') or sprint_period['start_datetime'].strftime('%Y-%m-%dT00:00:00')
                sprint_end_iso = sprint_period.get('end_iso') or sprint_period['end_datetime'].strftime('%Y-%m-%dT23:59:59')
                iteration_path = sprint_period.get('iteration_path') or project_config.get('iteration_path')
                
                print(f"   📅 Sprint Period: {sprint_period['start_date']} to {sprint_period['end_date']}")
                if sprint_period.get('iteration_name'):
                    print(f"   📋 Iteration: {sprint_period['iteration_name']}")
            else:
                # Fallback to config values
                sprint_period = Config.get_current_sprint_period()
                sprint_start_iso = sprint_period.get('start_iso') or sprint_period['start_datetime'].strftime('%Y-%m-%dT00:00:00')
                sprint_end_iso = sprint_period.get('end_iso') or sprint_period['end_datetime'].strftime('%Y-%m-%dT23:59:59')
                iteration_path = project_config.get('iteration_path')
                print(f"   ⚠️ Using default sprint period: {sprint_period['start_date']} to {sprint_period['end_date']}")
            
            result = get_work_item_count(org_name, project_name, tags, sprint_start_iso, sprint_end_iso, iteration_path)
            
            if result:
                # Store with organization prefix to avoid naming conflicts
                project_key = f"{org_name}_{project_name}"
                # Store sprint period info with the result
                if sprint_period:
                    result['sprint_period'] = {
                        'start_date': sprint_period.get('start_date'),
                        'end_date': sprint_period.get('end_date'),
                        'iteration_name': sprint_period.get('iteration_name'),
                        'iteration_path': sprint_period.get('iteration_path')
                    }
                all_results[project_key] = result
                print(f"      ✅ {project_name}: {result['total_items']} work items")
            else:
                print(f"      ❌ Failed to get data for {project_name}")
    
    # Save results to JSON file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'data/sprint_count_{timestamp}.json'
    
    # Create data directory if it doesn't exist
    import os
    os.makedirs('data', exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    # Print summary
    print(f"\n📊 Sprint Summary:")
    print(f"=" * 30)
    
    total_work_items = 0
    for project_key, result in all_results.items():
        count = result['total_items']
        total_work_items += count
        org_project = project_key.split('_', 1)
        display_name = f"{org_project[0]}/{org_project[1]}" if len(org_project) > 1 else project_key
        print(f"   {project_key}: {display_name}: {count} work items")
    
    print(f"   {'Total':>20}: {total_work_items} work items")
    print(f"\n🎯 Ready to generate HTML report!")

if __name__ == "__main__":
    main()