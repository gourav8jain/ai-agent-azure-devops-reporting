import json
import os
from datetime import datetime
from config import Config

def generate_compact_html_report(json_file):
    """Generate a compact HTML report optimized for email rendering"""
    
    # Load sprint data
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            sprint_data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading JSON file: {e}")
        return None
    
    # Validate sprint_data is not empty
    if not sprint_data:
        print(f"❌ JSON file contains no sprint data")
        return None
    
    # Validate sprint_data structure and check for actual work items
    total_work_items = 0
    for project_key, result in sprint_data.items():
        if not isinstance(result, dict):
            print(f"❌ Invalid data structure for project {project_key}")
            return None
        if 'total_items' not in result or 'engineer_metrics' not in result:
            print(f"❌ Missing required fields in project {project_key}")
            return None
        total_work_items += result.get('total_items', 0)
    
    if total_work_items == 0:
        print(f"❌ JSON file contains no work items (all zeros)")
        return None
    
    print(f"✅ Loaded sprint data: {len(sprint_data)} projects, {total_work_items} total work items")
    
    # Resolve sprint period dynamically - get overall period for header
    # Individual project periods will be shown in each project section
    overall_sprint_period = Config.get_current_sprint_period()
    sprint_start = overall_sprint_period['start_date']
    sprint_end = overall_sprint_period['end_date']
    
    # Calculate global status summary
    global_status_counts = {}
    for result in sprint_data.values():
        for engineer_metrics in result['engineer_metrics'].values():
            for state, count in engineer_metrics.get('states', {}).items():
                category = Config.get_state_category(state)
                global_status_counts[category] = global_status_counts.get(category, 0) + count
    
    # Generate compact HTML content with inline styles
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sprint Report - {datetime.now().strftime('%B %d, %Y')} - IOL Pay & VCC</title>
    <style>
        @media only screen and (max-width: 600px) {{
            .mobile-stack {{ display: block !important; width: 100% !important; }}
            .mobile-full {{ width: 100% !important; padding: 10px !important; }}
            .mobile-text {{ font-size: 14px !important; }}
            .mobile-padding {{ padding: 15px !important; }}
        }}
    </style>
</head>
<body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; color: #333;">
    <table style="width: 100%; max-width: 900px; margin: 0 auto; background: white; border-collapse: collapse;">
        <!-- Header -->
        <tr>
            <td style="background: #0078d4; color: white; padding: 20px; text-align: center;">
                <h1 style="margin: 0; font-size: 24px; font-weight: 600;">Sprint Report - {datetime.now().strftime('%B %d, %Y')} - IOL Pay & VCC</h1>
                <p style="margin: 5px 0 0 0; font-size: 14px;">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </td>
        </tr>
        
        <!-- Summary Cards -->
        <tr>
            <td style="padding: 20px;" class="mobile-padding">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="width: 33.33%; padding: 10px; text-align: center; vertical-align: top;" class="mobile-stack">
                            <div style="background: #f8f9fa; padding: 20px; border: 2px solid #0078d4; border-radius: 8px; margin-bottom: 10px;">
                                <h3 style="color: #333; font-size: 16px; margin: 0 0 10px 0; font-weight: 600;" class="mobile-text">Total Work Items</h3>
                                <div style="font-size: 28px; font-weight: 700; color: #0078d4; margin-bottom: 5px;">{sum(result['total_items'] for result in sprint_data.values())}</div>
                                <div style="color: #333; font-size: 14px; font-weight: 500;" class="mobile-text">Across all projects</div>
                            </div>
                        </td>
                        <td style="width: 33.33%; padding: 10px; text-align: center; vertical-align: top;" class="mobile-stack">
                            <div style="background: #f8f9fa; padding: 20px; border: 2px solid #0078d4; border-radius: 8px; margin-bottom: 10px;">
                                <h3 style="color: #333; font-size: 16px; margin: 0 0 10px 0; font-weight: 600;" class="mobile-text">Projects</h3>
                                <div style="font-size: 28px; font-weight: 700; color: #0078d4; margin-bottom: 5px;">{len(sprint_data)}</div>
                                <div style="color: #333; font-size: 14px; font-weight: 500;" class="mobile-text">Active projects in sprint</div>
                            </div>
                        </td>
                        <td style="width: 33.33%; padding: 10px; text-align: center; vertical-align: top;" class="mobile-stack">
                            <div style="background: #f8f9fa; padding: 20px; border: 2px solid #0078d4; border-radius: 8px; margin-bottom: 10px;">
                                <h3 style="color: #333; font-size: 16px; margin: 0 0 10px 0; font-weight: 600;" class="mobile-text">Engineers</h3>
                                <div style="font-size: 28px; font-weight: 700; color: #0078d4; margin-bottom: 5px;">{sum(len(result['engineer_metrics']) for result in sprint_data.values())}</div>
                                <div style="color: #333; font-size: 14px; font-weight: 500;" class="mobile-text">Team members involved</div>
                            </div>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
"""
    
    # Add project sections
    for project_key, result in sprint_data.items():
        # Extract organization and project from key (format: "IWTX_IOL_X" or "IOLPulse_VCCWallet")
        org_project = project_key.split('_', 1)
        if len(org_project) == 2:
            org_name, project_id = org_project
        else:
            org_name = "Unknown"
            project_id = project_key
        
        # Get project configuration from organizations
        project_config = None
        iteration_display = "Current Sprint"
        
        for org_key, org_config in Config.ORGANIZATIONS.items():
            if org_config['name'] == org_name:
                for proj_key, proj_config in org_config['projects'].items():
                    if proj_key == project_id:
                        project_config = proj_config
                        break
                break
        
        # Get display name and iteration info
        display_name = project_config['project_name'] if project_config else project_id
        tags = project_config['tags'] if project_config else []
        tag_display = f"Filtered by: {', '.join(tags)}" if tags else "All work items"
        
        # Get iteration display - prefer from sprint_period in result data
        if result.get('sprint_period'):
            sprint_info = result['sprint_period']
            if sprint_info.get('iteration_name'):
                iteration_name = sprint_info['iteration_name']
                start_date = sprint_info.get('start_date', '')
                end_date = sprint_info.get('end_date', '')
                iteration_display = f"{iteration_name} ({start_date} to {end_date})"
            else:
                start_date = sprint_info.get('start_date', '')
                end_date = sprint_info.get('end_date', '')
                iteration_display = f"Current Sprint ({start_date} to {end_date})"
        else:
            iteration_display = project_config.get('iteration_display', 'Current Sprint') if project_config else "Current Sprint"
        
        # Calculate status-level summary using abstraction mapping
        status_counts = {}
        for engineer_metrics in result['engineer_metrics'].values():
            for state, count in engineer_metrics.get('states', {}).items():
                category = Config.get_state_category(state)
                status_counts[category] = status_counts.get(category, 0) + count
        
        # Calculate values for template placeholders
        total_items = result['total_items']
        
        # Sort status counts by preferred display order first, then by count
        preferred_order = ['In Progress', 'To Do', 'Done', 'Ready for QA', 'QA in Progress', 'Ready for Release']
        def status_sort_key(item):
            status, count = item
            return (preferred_order.index(status) if status in preferred_order else len(preferred_order), -count, status)
        sorted_status_counts = sorted(status_counts.items(), key=status_sort_key)
        
        # Build status summary HTML (prepend Total card)
        status_html = ""
        total_status = sum(count for _, count in sorted_status_counts)
        status_html += f"""
                        <td style=\"width: 33.33%; padding: 0; text-align: center; vertical-align: top;\">
                            <div style=\"background: #e9f5ff; padding: 15px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); border-left: 3px solid #1976d2; min-height: 70px;\">
                                <div style=\"font-size: 14px; font-weight: 600; color: #1976d2; margin-bottom: 8px; text-align: center;\">Total</div>
                                <div style=\"font-size: 20px; font-weight: 700; color: #0b5cab; text-align: center;\">{total_status}</div>
                            </div>
                        </td>"""
        for i, (status, count) in enumerate(sorted_status_counts):
            cells_in_row = (i + 1)  # +1 because Total card already added at start
            if cells_in_row % 3 == 0:
                status_html += "</tr><tr>"
            status_html += f"""
                        <td style=\"width: 33.33%; padding: 0; text-align: center; vertical-align: top;\">
                            <div style=\"background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); border-left: 3px solid #0078d4; min-height: 70px;\">
                                <div style=\"font-size: 14px; font-weight: 600; color: #333; margin-bottom: 8px; text-align: center;\">{status}</div>
                                <div style=\"font-size: 20px; font-weight: 700; color: #0078d4; text-align: center;\">{count}</div>
                            </div>
                        </td>"""
        # Fill remaining cells if needed (considering Total)
        total_cells = 1 + len(sorted_status_counts)
        remaining_cells = 3 - (total_cells % 3)
        if remaining_cells < 3:
            for _ in range(remaining_cells):
                status_html += '<td style="width: 33.33%; padding: 0;"></td>'
        
        html_content += f"""
        <!-- Project Section: {display_name} -->
        <tr>
            <td style="padding: 20px; border-top: 2px solid #e9ecef;" class="mobile-padding">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="padding-bottom: 15px; border-bottom: 2px solid #0078d4;">
                            <h2 style="margin: 0 0 10px 0; color: #0078d4; font-size: 22px; font-weight: 600;" class="mobile-text">{display_name}</h2>
                            <div style="background: #e3f2fd; color: #1976d2; padding: 8px 15px; border-radius: 20px; font-size: 14px; font-weight: 500; display: inline-block; margin-right: 10px; margin-bottom: 5px;" class="mobile-text">{tag_display}</div>
                            <div style="background: #f3e5f5; color: #7b1fa2; padding: 8px 15px; border-radius: 20px; font-size: 14px; font-weight: 500; display: inline-block; margin-bottom: 5px;" class="mobile-text">{iteration_display}</div>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 15px 0;">
                            <div style="background: #f0f8ff; padding: 15px; border-radius: 8px; border: 1px solid #cce7ff; margin-bottom: 15px;">
                                <h3 style="color: #1976d2; font-size: 16px; margin: 0 0 15px 0; font-weight: 600;" class="mobile-text">Project Status Summary</h3>
                                <div style="display: flex; flex-wrap: wrap; gap: 15px; align-items: center;" class="mobile-text">
                                    <!-- Total pill -->
                                    <div style="background: #e9f5ff; color: #0b5cab; padding: 12px 16px; border-radius: 20px; font-size: 16px; font-weight: 600; border: 2px solid #b6e0ff; text-align: center; min-width: 80px;">
                                        <div style="font-size: 12px; font-weight: 500; margin-bottom: 4px;">Total</div>
                                        <div style="font-size: 24px; font-weight: 700; color: #0b5cab;">{total_items}</div>
                                    </div>
                                    {''.join([f'''
                                    <div style="background: {'#d4edda' if status == 'Done' else '#fff3cd' if status == 'In Progress' else '#f8f9fa'}; 
                                                color: {'#155724' if status == 'Done' else '#856404' if status == 'In Progress' else '#333'}; 
                                                padding: 12px 16px; border-radius: 20px; font-size: 16px; font-weight: 600; 
                                                border: 2px solid {'#c3e6cb' if status == 'Done' else '#ffeaa7' if status == 'In Progress' else '#dee2e6'}; 
                                                text-align: center; min-width: 80px;">
                                        <div style="font-size: 12px; font-weight: 500; margin-bottom: 4px;">{status}</div>
                                        <div style="font-size: 24px; font-weight: 700; color: {'#0f5132' if status == 'Done' else '#664d03' if status == 'In Progress' else '#0078d4'};">
                                            {count}
                                        </div>
                                    </div>''' for status, count in sorted_status_counts])}
                                </div>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 20px 0;">
                            <h3 style="color: #333; font-size: 18px; margin: 0 0 15px 0; font-weight: 600;" class="mobile-text">Engineer Breakdown with Task Details</h3>
                            <table style="width: 100%; border-collapse: collapse;">
"""
        
        # Generate engineer cards in compact 2x4 grid
        engineer_list = list(result['engineer_metrics'].items())
        
        # Generate engineer rows (mobile-friendly: 1 per row on mobile, 2 per row on desktop)
        for row_start in range(0, len(engineer_list), 2):
            html_content += "<tr>"
            for i in range(row_start, min(row_start + 2, len(engineer_list))):
                engineer, metrics = engineer_list[i]
                total_items = metrics.get('total_items', 0)
                states = metrics.get('states', {})
                
                # Generate state breakdown with abstraction mapping
                abstracted_engineer_states = {}
                for state, count in states.items():
                    category = Config.get_state_category(state)
                    abstracted_engineer_states[category] = abstracted_engineer_states.get(category, 0) + count
                
                # Sort abstracted states by count (include all statuses)
                sorted_abstracted_states = sorted(abstracted_engineer_states.items(), key=lambda x: x[1], reverse=True)
                
                # Calculate task completion percentage
                completed_tasks = abstracted_engineer_states.get('Done', 0)
                completion_percentage = round((completed_tasks / total_items * 100)) if total_items > 0 else 0
                
                # Create comprehensive task details
                task_details = f"Total Tasks: {total_items} | Completion: {completion_percentage}%"
                if len(sorted_abstracted_states) > 0:
                    top_status = sorted_abstracted_states[0]
                    task_details += f" | Top Status: {top_status[0]} ({top_status[1]})"
                
                # Create detailed status breakdown with highlighted numbers (include all statuses)
                status_breakdown = ""
                # Prepend Total chip
                status_breakdown += f'''\
                        <div style="background: #e9f5ff; color: #0b5cab; padding: 8px 12px; border-radius: 15px; font-size: 12px; font-weight: 600; 
                                    border: 2px solid #b6e0ff; display: inline-block; margin: 3px; text-align: center; min-width: 60px;">
                            <div style="font-size: 10px; font-weight: 500; margin-bottom: 2px;">Total</div>
                            <div style="font-size: 18px; font-weight: 700; color: #0b5cab;">{total_items}</div>
                        </div>'''
                for category, count in sorted_abstracted_states:
                    if category == 'Done':
                        status_breakdown += f'''
                        <div style="background: #d4edda; color: #155724; padding: 8px 12px; border-radius: 15px; font-size: 12px; font-weight: 600; 
                                    border: 2px solid #c3e6cb; display: inline-block; margin: 3px; text-align: center; min-width: 60px;">
                            <div style="font-size: 10px; font-weight: 500; margin-bottom: 2px;">{category}</div>
                            <div style="font-size: 18px; font-weight: 700; color: #0f5132;">{count}</div>
                        </div>'''
                    elif category == 'In Progress':
                        status_breakdown += f'''
                        <div style="background: #fff3cd; color: #856404; padding: 8px 12px; border-radius: 15px; font-size: 12px; font-weight: 600; 
                                    border: 2px solid #ffeaa7; display: inline-block; margin: 3px; text-align: center; min-width: 60px;">
                            <div style="font-size: 10px; font-weight: 500; margin-bottom: 2px;">{category}</div>
                            <div style="font-size: 18px; font-weight: 700; color: #664d03;">{count}</div>
                        </div>'''
                    else:
                        status_breakdown += f'''
                        <div style="background: #f8f9fa; color: #333; padding: 8px 12px; border-radius: 15px; font-size: 12px; font-weight: 600; 
                                    border: 2px solid #dee2e6; display: inline-block; margin: 3px; text-align: center; min-width: 60px;">
                            <div style="font-size: 10px; font-weight: 500; margin-bottom: 2px;">{category}</div>
                            <div style="font-size: 18px; font-weight: 700; color: #0078d4;">{count}</div>
                        </div>'''
                
                # Create pending-focused task lists for leadership visibility
                tasks = metrics.get('tasks', [])
                pending_summary = ""
                pending_list_html = ""
                completed_list_html = ""
                if tasks:
                    # Split tasks into pending (not Done) and completed (Done)
                    pending_categories = ['To Do', 'In Progress', 'Ready for QA', 'QA in Progress', 'Ready for Release']
                    pending_tasks = []
                    completed_tasks = []
                    pending_counts = {cat: 0 for cat in pending_categories}
                    for t in tasks:
                        cat = Config.get_state_category(t['state'])
                        if cat == 'Done':
                            completed_tasks.append(t)
                        else:
                            pending_tasks.append(t)
                            if cat in pending_counts:
                                pending_counts[cat] += 1

                    # Build pending summary like: Pending: N — In Progress 3, To Do 2, QA in Progress 1
                    total_pending = len(pending_tasks)
                    parts = [f"{cat} {count}" for cat, count in pending_counts.items() if count > 0]
                    pending_summary = f"Pending: {total_pending}" + (" — " + ", ".join(parts) if parts else "")

                    # Sort lists for readability
                    def by_title(t):
                        return t['title'].lower()
                    pending_tasks_sorted = sorted(pending_tasks, key=by_title)
                    completed_tasks_sorted = sorted(completed_tasks, key=by_title)

                    if pending_tasks_sorted:
                        items = [f"• {t['title']} ({Config.get_state_category(t['state'])})" for t in pending_tasks_sorted]
                        pending_list_html = "<br>".join(items)
                    if completed_tasks_sorted:
                        items = [f"• {t['title']} ({Config.get_state_category(t['state'])})" for t in completed_tasks_sorted]
                        completed_list_html = "<br>".join(items)
                else:
                    pending_summary = "No task details available"
                
                html_content += f"""
                        <td style="width: 50%; padding: 10px; vertical-align: top;" class="mobile-full">
                            <div style="background: #f8f9fa; padding: 20px; border: 2px solid #0078d4; border-radius: 8px; margin: 5px;">
                                <h4 style="margin: 0 0 15px 0; color: #0078d4; font-size: 18px; font-weight: 600;" class="mobile-text">{engineer}</h4>
                                <div style="background: #e8f4fd; padding: 15px; border-radius: 6px; margin-bottom: 15px; border: 1px solid #b3d9f2;">
                                    <div style="font-size: 16px; color: #1976d2; font-weight: 600; margin-bottom: 8px;" class="mobile-text">Task Summary</div>
                                    <div style="font-size: 14px; color: #333; line-height: 1.5; margin-bottom: 8px;" class="mobile-text">{task_details}</div>
                                    <div style="font-size: 14px; color: #333; line-height: 1.5; margin-bottom: 8px;" class="mobile-text">All Statuses: {status_breakdown}</div>
                                </div>
                                <div style="background: #f0f8ff; padding: 15px; border-radius: 6px; border: 1px solid #cce7ff;">
                                    <div style="font-size: 16px; color: #1976d2; font-weight: 600; margin-bottom: 6px;" class="mobile-text">Key Tasks</div>
                                    <div style="font-size: 13px; color: #0b5cab; font-weight: 600; margin-bottom: 6px;" class="mobile-text">{pending_summary}</div>
                                    {f'<div style="font-size: 13px; color: #333; line-height: 1.4; margin-bottom: 8px;" class="mobile-text">{pending_list_html}</div>' if pending_list_html else ''}
                                    {f'<div style="font-size: 13px; color: #2e7d32; font-weight: 600; margin-top: 4px;" class="mobile-text">Completed</div>' if completed_list_html else ''}
                                    {f'<div style="font-size: 13px; color: #333; line-height: 1.4;" class="mobile-text">{completed_list_html}</div>' if completed_list_html else ''}
                                </div>
                            </div>
                        </td>"""
            
            # Fill remaining cell if odd number of engineers
            if len(engineer_list) % 2 == 1 and row_start == len(engineer_list) - 1:
                html_content += '<td style="width: 50%; padding: 10px;" class="mobile-full"></td>'
            
            html_content += "</tr>"
        
        html_content += """
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
"""
    
    # Add footer
    html_content += f"""
        <tr>
            <td style="background: #f8f9fa; padding: 20px; text-align: center; color: #333; font-size: 14px; font-weight: 500;">
                Generated by <span style="color: #0078d4; font-weight: 600;">Azure DevOps AI Agent</span>
            </td>
        </tr>
    </table>
</body>
</html>"""
    
    return html_content

def main():
    """Main function to generate compact HTML report"""
    print("🎨 Compact HTML Report Generator")
    print("=" * 40)
    
    # Find the most recent sprint count file
    data_dir = 'data'
    json_files = []
    
    if os.path.exists(data_dir):
        json_files = [f for f in os.listdir(data_dir) if f.startswith('sprint_count_') and f.endswith('.json')]
    
    # Also check current directory for backward compatibility
    if not json_files:
        json_files = [f for f in os.listdir('.') if f.startswith('sprint_count_') and f.endswith('.json')]
    
    if not json_files:
        print("❌ No sprint count files found. Run get_sprint_count.py first.")
        return
    
    # Get the latest file with full path
    latest_file = max(json_files, key=lambda x: os.path.getctime(os.path.join(data_dir, x)) if os.path.exists(data_dir) else os.path.getctime(x))
    
    # Use full path if file is in data directory
    if os.path.exists(os.path.join(data_dir, latest_file)):
        latest_file = os.path.join(data_dir, latest_file)
    
    print(f"📁 Using data from: {latest_file}")
    
    # Generate compact HTML report
    html_content = generate_compact_html_report(latest_file)
    
    if html_content:
        # Save HTML report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'compact_sprint_report_{timestamp}.html'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Compact HTML report generated: {output_file}")
        print(f"📊 Report size: {len(html_content)} characters")
        print(f"🌐 Open {output_file} in your browser to view the report")
        print(f"📧 Ready to send via email!")
    else:
        print("❌ Failed to generate HTML report")

if __name__ == "__main__":
    main()
