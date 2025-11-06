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
        # First, get teams for the project - try multiple API endpoints
        teams = []
        target_team = None
        
        # Try Core API first (more reliable)
        try:
            core_teams_url = f"https://dev.azure.com/{organization}/_apis/projects/{project}/teams?api-version=7.0"
            response = requests.get(core_teams_url, headers=headers)
            response.raise_for_status()
            teams_data = response.json()
            teams = teams_data.get('value', [])
            print(f"   ✅ Found {len(teams)} teams via Core API")
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️ Core API failed: {str(e)}")
            # Fallback to project-scoped teams API
            try:
                teams_url = f"https://dev.azure.com/{organization}/{project}/_apis/teams?api-version=7.0"
                response = requests.get(teams_url, headers=headers)
                response.raise_for_status()
                teams_data = response.json()
                teams = teams_data.get('value', [])
                print(f"   ✅ Found {len(teams)} teams via Teams API")
            except requests.exceptions.RequestException as e2:
                print(f"   ⚠️ Teams API also failed: {str(e2)}")
                # Last resort: try to get default team
                try:
                    default_team_url = f"https://dev.azure.com/{organization}/{project}/_apis/core/teams?api-version=7.0"
                    response = requests.get(default_team_url, headers=headers)
                    if response.status_code == 200:
                        teams_data = response.json()
                        teams = teams_data.get('value', [])
                        print(f"   ✅ Found {len(teams)} teams via Core Teams API")
                except:
                    pass
        
        # Find the team by name if provided
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
            print(f"   💡 Will use fallback iteration path from configuration")
            return None
        
        team_id = target_team.get('id')
        print(f"   ✅ Using team: {target_team.get('name')} (ID: {team_id})")
        
        # Get ALL iterations for the team (not just current)
        iterations_url = f"https://dev.azure.com/{organization}/{project}/{team_id}/_apis/work/teamsettings/iterations?api-version=7.0"
        response = requests.get(iterations_url, headers=headers)
        response.raise_for_status()
        iterations_data = response.json()
        all_iterations = iterations_data.get('value', [])
        
        print(f"   📋 Found {len(all_iterations)} total iterations/sprints")
        
        if not all_iterations:
            print(f"   ⚠️ No iterations found for team {target_team.get('name')}")
            return None
        
        # Find current iteration based on today's date
        today = datetime.now().date()
        current_iteration = None
        past_iterations = []
        future_iterations = []
        
        # Parse and categorize all iterations
        print(f"   📋 Processing {len(all_iterations)} iterations/sprints to find current one...")
        for iteration in all_iterations:
            attrs = iteration.get('attributes', {})
            start_date_str = attrs.get('startDate')
            end_date_str = attrs.get('finishDate')
            iteration_name = iteration.get('name', 'Unknown')
            iteration_path = iteration.get('path', 'Unknown')
            
            if not start_date_str or not end_date_str:
                print(f"      ⚠️ Skipping {iteration_name} (missing dates)")
                continue
            
            # Parse dates from Azure DevOps format
            if isinstance(start_date_str, str):
                try:
                    if 'T' in start_date_str:
                        start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00')).date()
                    else:
                        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                except Exception as e:
                    print(f"      ⚠️ Skipping {iteration_name} (date parse error: {e})")
                    continue
            else:
                continue
            
            if isinstance(end_date_str, str):
                try:
                    if 'T' in end_date_str:
                        end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00')).date()
                    else:
                        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                except Exception as e:
                    print(f"      ⚠️ Skipping {iteration_name} (end date parse error: {e})")
                    continue
            else:
                continue
            
            # Check if today is within this iteration
            if start_date <= today <= end_date:
                current_iteration = {
                    'id': iteration.get('id'),
                    'name': iteration_name,
                    'path': iteration_path,
                    'start_date': start_date_str,
                    'end_date': end_date_str
                }
                print(f"   ✅ Found CURRENT iteration: {iteration_name} ({start_date} to {end_date})")
                print(f"      📋 Path: {iteration_path}")
                break
            elif end_date < today:
                past_iterations.append({
                    'iteration': iteration,
                    'end_date': end_date,
                    'start_date': start_date,
                    'name': iteration_name,
                    'path': iteration_path
                })
                print(f"      📅 Past: {iteration_name} ({start_date} to {end_date})")
            elif start_date > today:
                future_iterations.append({
                    'iteration': iteration,
                    'start_date': start_date,
                    'end_date': end_date,
                    'name': iteration_name,
                    'path': iteration_path
                })
                print(f"      🔮 Future: {iteration_name} ({start_date} to {end_date})")
        
        # If no current iteration, use the most recent past iteration
        if not current_iteration:
            if past_iterations:
                # Sort by end_date descending to get most recent past iteration
                past_iterations.sort(key=lambda x: x['end_date'], reverse=True)
                most_recent = past_iterations[0]['iteration']
                attrs = most_recent.get('attributes', {})
                current_iteration = {
                    'id': most_recent.get('id'),
                    'name': most_recent.get('name'),
                    'path': most_recent.get('path'),
                    'start_date': attrs.get('startDate'),
                    'end_date': attrs.get('finishDate')
                }
                print(f"   ⚠️ No active iteration found. Using most recent past iteration: {current_iteration['name']}")
                print(f"      📋 Path: {current_iteration['path']}")
            elif future_iterations:
                # If no past iterations, use the nearest future iteration
                future_iterations.sort(key=lambda x: x['start_date'])
                nearest_future = future_iterations[0]['iteration']
                attrs = nearest_future.get('attributes', {})
                current_iteration = {
                    'id': nearest_future.get('id'),
                    'name': nearest_future.get('name'),
                    'path': nearest_future.get('path'),
                    'start_date': attrs.get('startDate'),
                    'end_date': attrs.get('finishDate')
                }
                print(f"   ⚠️ No active iteration found. Using nearest future iteration: {current_iteration['name']}")
                print(f"      📋 Path: {current_iteration['path']}")
        
        if not current_iteration:
            print(f"   ❌ No iteration found for team {target_team.get('name')}")
        else:
            print(f"   ✅ Selected iteration: {current_iteration['name']} (Path: {current_iteration['path']})")
        
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

    # Use iteration path filtering if available (preferred)
    if iteration_path:
        # Try exact match first - don't escape, use the path as-is
        # Azure DevOps WIQL handles backslashes in iteration paths
        wiql_query["query"] += f"""
        AND [System.IterationPath] = '{iteration_path}'
        """
        print(f"   📋 Iteration path filtering (exact match): {iteration_path}")
        
        # If we also have date range, add it as additional filter for safety
        if sprint_start and sprint_end:
            date_start = sprint_start.split('T', 1)[0]
            date_end = sprint_end.split('T', 1)[0]
            wiql_query["query"] += f"""
        AND [System.ChangedDate] >= '{date_start}'
        AND [System.ChangedDate] <= '{date_end}'
        """
            print(f"   📅 Also using date filtering: {date_start} to {date_end}")
    elif sprint_start and sprint_end:
        # Add date range filtering as fallback (when no iteration path available)
        date_start = sprint_start.split('T', 1)[0]
        date_end = sprint_end.split('T', 1)[0]
        wiql_query["query"] += f"""
        AND [System.ChangedDate] >= '{date_start}'
        AND [System.ChangedDate] <= '{date_end}'
        """
        print(f"   📅 Date filtering: {date_start} to {date_end}")
    else:
        # No filtering - will get all work items (not recommended but handled)
        print(f"   ⚠️ No iteration path or date range specified - fetching all work items")

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
    
    # Print the full query for debugging
    print(f"   🔍 Full WIQL Query:")
    print(f"      {wiql_query['query']}")
    
    try:
        response = requests.post(wiql_url, headers=headers, json=wiql_query)
        response.raise_for_status()
        
        wiql_result = response.json()
        work_item_ids = [item['id'] for item in wiql_result.get('workItems', [])]
        
        print(f"   📊 Found {len(work_item_ids)} work items")
        
        # If no work items found with exact match and we have iteration path, try UNDER clause
        if not work_item_ids and iteration_path:
            print(f"   ⚠️ No work items found with exact match, trying UNDER clause...")
            wiql_query_under = wiql_query.copy()
            # Replace the iteration path condition with UNDER
            original_query = wiql_query_under["query"]
            # Remove the old iteration path condition
            original_query = original_query.replace(f"AND [System.IterationPath] = '{iteration_path}'", "")
            # Remove date filters if present (to make UNDER work better)
            import re
            original_query = re.sub(r'AND \[System\.ChangedDate\].*?\n', '', original_query)
            # Add UNDER clause
            wiql_query_under["query"] = original_query + f"\n        AND [System.IterationPath] UNDER '{iteration_path}'"
            print(f"   🔍 Trying WIQL Query with UNDER:")
            print(f"      {wiql_query_under['query']}")
            
            try:
                response_under = requests.post(wiql_url, headers=headers, json=wiql_query_under)
                response_under.raise_for_status()
                wiql_result_under = response_under.json()
                work_item_ids = [item['id'] for item in wiql_result_under.get('workItems', [])]
                print(f"   📊 Found {len(work_item_ids)} work items with UNDER clause")
            except Exception as e:
                print(f"   ⚠️ UNDER clause also failed: {str(e)}")
        
        # If still no work items and we have iteration path, try date-only filtering as fallback
        if not work_item_ids and iteration_path and sprint_start and sprint_end:
            print(f"   ⚠️ Iteration path '{iteration_path}' may not exist, trying date-only filtering...")
            date_start = sprint_start.split('T', 1)[0]
            date_end = sprint_end.split('T', 1)[0]
            wiql_query_date = {
                'query': f"""
        SELECT [System.Id]
        FROM WorkItems 
        WHERE [System.TeamProject] = @project
        AND [System.ChangedDate] >= '{date_start}'
        AND [System.ChangedDate] <= '{date_end}'
        """
            }
            if tags:
                tag_conditions = []
                for tag in tags:
                    tag_conditions.append(f"[System.Tags] CONTAINS WORDS '{tag}'")
                if tag_conditions:
                    wiql_query_date["query"] += f" AND ({' OR '.join(tag_conditions)})"
            
            try:
                response_date = requests.post(wiql_url, headers=headers, json=wiql_query_date)
                response_date.raise_for_status()
                wiql_result_date = response_date.json()
                work_item_ids = [item['id'] for item in wiql_result_date.get('workItems', [])]
                print(f"   📊 Found {len(work_item_ids)} work items with date-only filtering")
            except Exception as e:
                print(f"   ⚠️ Date-only filtering also failed: {str(e)}")
        
        if not work_item_ids:
            if iteration_path:
                print(f"   ⚠️ No work items found for iteration path: {iteration_path}")
                print(f"   💡 The iteration path may not exist in Azure DevOps. Please verify it exists.")
            else:
                print(f"   ⚠️ No work items found for the specified criteria")
            return {'total_items': 0, 'engineer_metrics': {}}
        
        # Get detailed work item information
        return get_engineer_metrics(organization, project, work_item_ids, headers)
        
    except requests.exceptions.RequestException as e:
        error_message = str(e)
        error_response = None
        
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_response = e.response.json()
                error_message_detail = error_response.get('message', '')
                # Check if it's an iteration path error
                if 'iteration path does not exist' in error_message_detail.lower() or 'TF51011' in str(error_response):
                    print(f"   ⚠️ Iteration path does not exist: {iteration_path}")
                    # Try date-only filtering as fallback
                    if iteration_path and sprint_start and sprint_end:
                        print(f"   💡 Falling back to date-only filtering...")
                        date_start = sprint_start.split('T', 1)[0]
                        date_end = sprint_end.split('T', 1)[0]
                        wiql_query_date = {
                            'query': f"""
        SELECT [System.Id]
        FROM WorkItems 
        WHERE [System.TeamProject] = @project
        AND [System.ChangedDate] >= '{date_start}'
        AND [System.ChangedDate] <= '{date_end}'
        """
                        }
                        if tags:
                            tag_conditions = []
                            for tag in tags:
                                tag_conditions.append(f"[System.Tags] CONTAINS WORDS '{tag}'")
                            if tag_conditions:
                                wiql_query_date["query"] += f" AND ({' OR '.join(tag_conditions)})"
                        
                        try:
                            response_date = requests.post(wiql_url, headers=headers, json=wiql_query_date)
                            response_date.raise_for_status()
                            wiql_result_date = response_date.json()
                            work_item_ids = [item['id'] for item in wiql_result_date.get('workItems', [])]
                            print(f"   ✅ Found {len(work_item_ids)} work items using date-only filtering")
                            if work_item_ids:
                                return get_engineer_metrics(organization, project, work_item_ids, headers)
                        except Exception as e2:
                            print(f"   ⚠️ Date-only fallback also failed: {str(e2)}")
                    return {'total_items': 0, 'engineer_metrics': {}}
            except:
                pass
        
        print(f"   ❌ Error querying work items: {error_message}")
        if error_response:
            print(f"   ❌ Error details: {error_response}")
        elif hasattr(e, 'response') and e.response is not None:
            print(f"   ❌ Error response: {e.response.text}")
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
            
            if sprint_period and not sprint_period.get('fallback'):
                # Got actual dates from Azure DevOps
                sprint_start_iso = sprint_period.get('start_iso') or sprint_period['start_datetime'].strftime('%Y-%m-%dT00:00:00')
                sprint_end_iso = sprint_period.get('end_iso') or sprint_period['end_datetime'].strftime('%Y-%m-%dT23:59:59')
                iteration_path = sprint_period.get('iteration_path') or project_config.get('iteration_path')
                
                print(f"   📅 Sprint Period: {sprint_period['start_date']} to {sprint_period['end_date']}")
                if sprint_period.get('iteration_name'):
                    print(f"   📋 Iteration: {sprint_period['iteration_name']}")
            elif sprint_period and sprint_period.get('fallback'):
                # Fallback: Use calculated iteration path with date filtering if available
                iteration_path = sprint_period.get('iteration_path') or project_config.get('iteration_path')
                # Use date filtering as well if we have dates from fallback calculation
                if sprint_period.get('start_datetime') and sprint_period.get('end_datetime'):
                    sprint_start_iso = sprint_period.get('start_iso') or sprint_period['start_datetime'].strftime('%Y-%m-%dT00:00:00')
                    sprint_end_iso = sprint_period.get('end_iso') or sprint_period['end_datetime'].strftime('%Y-%m-%dT23:59:59')
                    print(f"   ⚠️ Using fallback iteration path: {iteration_path}")
                    print(f"   📅 Sprint Period: {sprint_period['start_date']} to {sprint_period['end_date']}")
                    print(f"   📋 Iteration: {sprint_period.get('iteration_name', 'Unknown')}")
                    print(f"   ⚠️ Will use BOTH iteration path and date filtering")
                else:
                    sprint_start_iso = None
                    sprint_end_iso = None
                    print(f"   ⚠️ Using fallback iteration path: {iteration_path}")
                    print(f"   ⚠️ Will filter by iteration path only (no date filtering)")
            else:
                # Fallback to config values if nothing works
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