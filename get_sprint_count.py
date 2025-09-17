import requests
import json
import base64
from datetime import datetime
from config import Config

def get_work_item_count(project, tags=None, sprint_start=None, sprint_end=None):
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
    
    print(f"\n🔍 Querying {project} project...")
    
    # Get project configuration; prefer date range filtering
    project_config = Config.get_project_config(project)
    iteration_path = project_config.get('iteration_path') if project_config else None

    wiql_query = {
        'query': f"""
        SELECT [System.Id]
        FROM WorkItems 
        WHERE [System.TeamProject] = @project
        """
    }

    # Add iteration path filtering if available
    # Always use date range filtering to avoid mismatched iteration names
    # Convert to ISO if provided
    # Use date-only format for broad compatibility
    date_start = sprint_start.split('T', 1)[0]
    date_end = sprint_end.split('T', 1)[0]
    wiql_query["query"] += f"""
        AND [System.ChangedDate] >= '{date_start}'
        AND [System.ChangedDate] <= '{date_end}'
        """
    print(f"   📅 Date filtering: {date_start} to {date_end}")
    # Debug: show final WIQL
    print("   📝 WIQL query:")
    print(wiql_query["query"])

    # Add tag filtering if specified
    if tags:
        tag_conditions = []
        for tag in tags:
            tag_conditions.append(f"[System.Tags] CONTAINS WORDS '{tag}'")

        if tag_conditions:
            wiql_query["query"] += f" AND ({' OR '.join(tag_conditions)})"
            print(f"   🏷️ Filtering by tags: {', '.join(tags)}")
        else:
            print(f"   ⚠️ No tag conditions generated")
    else:
        print(f"   ℹ️ No tags specified for filtering")

    # Execute WIQL query
    wiql_url = f"https://dev.azure.com/{Config.AZURE_DEVOPS_ORG}/{project}/_apis/wit/wiql?api-version=7.0"
    
    try:
        response = requests.post(wiql_url, headers=headers, json=wiql_query)
        response.raise_for_status()
        
        wiql_result = response.json()
        work_item_ids = [item['id'] for item in wiql_result.get('workItems', [])]
        
        print(f"   📊 Found {len(work_item_ids)} work items")
        
        if not work_item_ids:
            return {'total_items': 0, 'engineer_metrics': {}}
        
        # Get detailed work item information
        return get_engineer_metrics(project, work_item_ids, headers)
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error querying work items: {str(e)}")
        return None

def get_engineer_metrics(project, work_item_ids, headers):
    """Get engineer-wise metrics for work items"""
    
    # Get work item details in batches
    batch_size = 200
    all_work_items = []
    
    for i in range(0, len(work_item_ids), batch_size):
        batch_ids = work_item_ids[i:i + batch_size]
        ids_param = ','.join(map(str, batch_ids))
        
        work_items_url = f"https://dev.azure.com/{Config.AZURE_DEVOPS_ORG}/{project}/_apis/wit/workitems?ids={ids_param}&$fields=System.Id,System.AssignedTo,System.State,System.Tags&api-version=7.0"
        
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
        
        # Get assignee name
        if assigned_to and 'displayName' in assigned_to:
            assignee = assigned_to['displayName']
        else:
            assignee = 'Unassigned'
        
        # Initialize engineer metrics if not exists
        if assignee not in engineer_metrics:
            engineer_metrics[assignee] = {
                'total_items': 0,
                'states': {}
            }
        
        # Update metrics
        engineer_metrics[assignee]['total_items'] += 1
        engineer_metrics[assignee]['states'][state] = engineer_metrics[assignee]['states'].get(state, 0) + 1
        
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
    
    # Get current sprint period dynamically
    sprint_period = Config.get_current_sprint_period()
    sprint_start_iso = sprint_period.get('start_iso') or sprint_period['start_datetime'].strftime('%Y-%m-%dT00:00:00')
    sprint_end_iso = sprint_period.get('end_iso') or sprint_period['end_datetime'].strftime('%Y-%m-%dT23:59:59')
    
    print(f"📅 Current Sprint Period: {sprint_period['start_date']} to {sprint_period['end_date']}")
    print(f"📅 Sprint calculated based on current date: {datetime.now().strftime('%d-%b-%Y')}")
    
    # Get counts for each project
    all_results = {}
    projects_config = Config.get_projects_config()
    
    for project_key, project_config in projects_config.items():
        project_name = project_key
        tags = project_config['tags']
        
        print(f"\n🏢 Processing project: {project_name}")
        
        result = get_work_item_count(project_name, tags, sprint_start_iso, sprint_end_iso)
        
        if result:
            all_results[project_name] = result
            print(f"   ✅ {project_name}: {result['total_items']} work items")
        else:
            print(f"   ❌ Failed to get data for {project_name}")
    
    # Save results to JSON file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'sprint_count_{timestamp}.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    # Print summary
    print(f"\n📊 Sprint Summary:")
    print(f"=" * 30)
    
    total_work_items = 0
    for project_name, result in all_results.items():
        count = result['total_items']
        total_work_items += count
        print(f"   {project_name}: {count} work items")
    
    print(f"   {'Total':>20}: {total_work_items} work items")
    print(f"\n🎯 Ready to generate HTML report!")

if __name__ == "__main__":
    main()
