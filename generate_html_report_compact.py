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
    
    # Resolve sprint period dynamically
    sprint_period = Config.get_current_sprint_period()
    sprint_start = sprint_period['start_date']
    sprint_end = sprint_period['end_date']
    
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
    <title>Azure DevOps Sprint Report</title>
</head>
<body style="font-family: Arial, sans-serif; margin: 0; padding: 10px; background-color: #f5f5f5; color: #333;">
    <div style="max-width: 900px; margin: 0 auto; background: white; border-radius: 6px; box-shadow: 0 1px 5px rgba(0,0,0,0.1); overflow: hidden;">
        <!-- Header -->
        <div style="background: #0078d4; color: white; padding: 15px; text-align: center;">
            <h1 style="margin: 0; font-size: 22px; font-weight: 300;">[REPORT] Azure DevOps Sprint Report</h1>
            <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 13px;">Sprint Period: {sprint_start} to {sprint_end}</p>
            <p style="margin: 3px 0 0 0; opacity: 0.9; font-size: 13px;">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <!-- Concise Task Summary -->
        <div style="margin: 15px 10px; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; color: white;">
            <h2 style="margin: 0 0 15px 0; font-size: 18px; font-weight: 600; text-align: center;">[OVERVIEW] Sprint Task Overview</h2>
            <div style="display: flex; justify-content: space-around; text-align: center; flex-wrap: wrap; margin-bottom: 15px;">
                <div style="flex: 1; min-width: 120px; margin: 5px;">
                    <div style="font-size: 20px; font-weight: 700; margin-bottom: 5px;">{sum(result['total_items'] for result in sprint_data.values())}</div>
                    <div style="font-size: 12px; opacity: 0.9;">Total Tasks</div>
                </div>
                <div style="flex: 1; min-width: 120px; margin: 5px;">
                    <div style="font-size: 20px; font-weight: 700; margin-bottom: 5px;">{len(sprint_data)}</div>
                    <div style="font-size: 12px; opacity: 0.9;">Projects</div>
                </div>
                <div style="flex: 1; min-width: 120px; margin: 5px;">
                    <div style="font-size: 20px; font-weight: 700; margin-bottom: 5px;">{sum(len(result['engineer_metrics']) for result in sprint_data.values())}</div>
                    <div style="font-size: 12px; opacity: 0.9;">Engineers</div>
                </div>
                <div style="flex: 1; min-width: 120px; margin: 5px;">
                    <div style="font-size: 20px; font-weight: 700; margin-bottom: 5px;">{sprint_start} to {sprint_end}</div>
                    <div style="font-size: 12px; opacity: 0.9;">Sprint Period</div>
                </div>
            </div>
            <!-- Status Breakdown -->
            <div style="background: rgba(255,255,255,0.1); border-radius: 6px; padding: 10px; margin-top: 10px;">
                <div style="font-size: 14px; font-weight: 600; margin-bottom: 8px; text-align: center;">[BREAKDOWN] Status Breakdown</div>
                <div style="display: flex; justify-content: space-around; text-align: center; flex-wrap: wrap;">
                    {''.join([f'''
                    <div style="flex: 1; min-width: 80px; margin: 3px;">
                        <div style="font-size: 16px; font-weight: 700; margin-bottom: 2px;">{count}</div>
                        <div style="font-size: 10px; opacity: 0.8;">{status}</div>
                    </div>''' for status, count in sorted(global_status_counts.items(), key=lambda x: x[1], reverse=True)[:6]])}
                </div>
            </div>
        </div>
        
        <!-- Summary Cards -->
        <div style="margin: 15px 0; padding: 0 10px;">
            <table style="width: 100%; border-collapse: separate; border-spacing: 10px; margin: 0 auto;">
                <tr>
                    <td style="width: 33.33%; padding: 0; text-align: center; vertical-align: top;">
                        <div style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 4px solid #0078d4; min-height: 80px;">
                            <h3 style="color: #333; font-size: 14px; margin-bottom: 8px; font-weight: 600; text-align: center;">[ITEMS] Total Work Items</h3>
                            <div style="font-size: 24px; font-weight: 700; color: #0078d4; margin-bottom: 5px; text-align: center;">{sum(result['total_items'] for result in sprint_data.values())}</div>
                            <div style="color: #666; font-size: 12px; text-align: center;">Across all projects</div>
                        </div>
                    </td>
                    <td style="width: 33.33%; padding: 0; text-align: center; vertical-align: top;">
                        <div style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 4px solid #0078d4; min-height: 80px;">
                            <h3 style="color: #333; font-size: 14px; margin-bottom: 8px; font-weight: 600; text-align: center;">[PROJECTS] Projects</h3>
                            <div style="font-size: 24px; font-weight: 700; color: #0078d4; margin-bottom: 5px; text-align: center;">{len(sprint_data)}</div>
                            <div style="color: #666; font-size: 12px; text-align: center;">Active projects in sprint</div>
                        </div>
                    </td>
                    <td style="width: 33.33%; padding: 0; text-align: center; vertical-align: top;">
                        <div style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 4px solid #0078d4; min-height: 80px;">
                            <h3 style="color: #333; font-size: 14px; margin-bottom: 8px; font-weight: 600; text-align: center;">[TEAM] Engineers</h3>
                            <div style="font-size: 24px; font-weight: 700; color: #0078d4; margin-bottom: 5px; text-align: center;">{sum(len(result['engineer_metrics']) for result in sprint_data.values())}</div>
                            <div style="color: #666; font-size: 12px; text-align: center;">Team members involved</div>
                        </div>
                    </td>
                </tr>
            </table>
        </div>
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
        
        # Get iteration display
        iteration_display = project_config.get('iteration_display', 'Current Sprint') if project_config else "Current Sprint"
        
        # Calculate status-level summary using abstraction mapping
        status_counts = {}
        for engineer_metrics in result['engineer_metrics'].values():
            for state, count in engineer_metrics.get('states', {}).items():
                category = Config.get_state_category(state)
                status_counts[category] = status_counts.get(category, 0) + count
        
        # Calculate values for template placeholders
        total_items = result['total_items']
        engineer_count = len(result['engineer_metrics'])
        status_count = len(status_counts)
        
        # Make sprint dates available in the template
        sprint_start_date = sprint_start
        sprint_end_date = sprint_end
        
        # Sort status counts by count
        sorted_status_counts = sorted(status_counts.items(), key=lambda x: x[1], reverse=True)
        
        html_content += f"""
        <!-- Project Section: {display_name} -->
        <div style="padding: 20px; border-bottom: 1px solid #e9ecef;">
            <div style="margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid #e9ecef;">
                <h2 style="margin: 0 0 8px 0; color: #0078d4; font-size: 20px; font-weight: 600;">{display_name}</h2>
                <span style="background: #e3f2fd; color: #1976d2; padding: 6px 12px; border-radius: 15px; font-size: 12px; font-weight: 500; display: inline-block;">{tag_display}</span>
                <div style="background: #f3e5f5; color: #7b1fa2; padding: 6px 12px; border-radius: 15px; font-size: 12px; font-weight: 500; margin-top: 8px; display: inline-block;">[SPRINT] {iteration_display}</div>
            </div>
            
            <!-- Status Summary -->
            <div style="margin-bottom: 20px;">
                <h3 style="color: #333; font-size: 16px; margin-bottom: 15px; font-weight: 600;">[STATUS] Status Level Summary</h3>
                <table style="width: 100%; border-collapse: separate; border-spacing: 10px; margin: 0 auto;">
                    <tr>"""
        
        # Add status items in rows of 3
        for i, (status, count) in enumerate(sorted_status_counts):
            if i > 0 and i % 3 == 0:
                html_content += "</tr><tr>"
            html_content += f"""
                        <td style="width: 33.33%; padding: 0; text-align: center; vertical-align: top;">
                            <div style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); border-left: 3px solid #0078d4; min-height: 70px;">
                                <div style="font-size: 14px; font-weight: 600; color: #333; margin-bottom: 8px; text-align: center;">{status}</div>
                                <div style="font-size: 20px; font-weight: 700; color: #0078d4; text-align: center;">{count}</div>
                            </div>
                        </td>"""
        
        # Fill remaining cells if needed
        remaining_cells = 3 - (len(sorted_status_counts) % 3)
        if remaining_cells < 3:
            for _ in range(remaining_cells):
                html_content += '<td style="width: 33.33%; padding: 0;"></td>'
        
        html_content += """
                    </tr>
                </table>
            </div>
            
            <!-- Task Summary -->
            <div style="margin-bottom: 20px;">
                <h3 style="color: #333; font-size: 16px; margin-bottom: 15px; font-weight: 600;">[TASKS] Task Summary</h3>
                <div style="background: #f8f9fa; border-radius: 8px; padding: 15px; border-left: 4px solid #28a745;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span style="font-size: 14px; font-weight: 600; color: #333;">Total Tasks in Current Sprint</span>
                        <span style="font-size: 18px; font-weight: 700; color: #28a745; background: white; padding: 6px 12px; border-radius: 6px; border: 1px solid #dee2e6;">{total_items}</span>
                    </div>
                    <div style="font-size: 12px; color: #666; line-height: 1.4;">
                        <strong>Active Engineers:</strong> {engineer_count} | 
                        <strong>Status Categories:</strong> {status_count} | 
                        <strong>Sprint Period:</strong> {sprint_start_date} to {sprint_end_date}
                    </div>
                </div>
            </div>
            
            <!-- Engineer Breakdown -->
            <div>
                <h3 style="color: #333; font-size: 16px; margin-bottom: 15px; font-weight: 600;">[ENGINEERS] Engineer Level Breakdown</h3>
                <table style="width: 100%; border-collapse: separate; border-spacing: 10px; margin: 0 auto;">
"""
        
        # Generate engineer cards in compact 2x4 grid
        engineer_list = list(result['engineer_metrics'].items())
        
        # First row (first 4 engineers)
        html_content += "<tr>"
        for i in range(min(4, len(engineer_list))):
            engineer, metrics = engineer_list[i]
            total_items = metrics.get('total_items', 0)
            states = metrics.get('states', {})
            
            # Generate state breakdown with abstraction mapping
            abstracted_engineer_states = {}
            for state, count in states.items():
                category = Config.get_state_category(state)
                abstracted_engineer_states[category] = abstracted_engineer_states.get(category, 0) + count
            
            # Sort abstracted states by count and show only top 3
            sorted_abstracted_states = sorted(abstracted_engineer_states.items(), key=lambda x: x[1], reverse=True)
            
            state_breakdown = ""
            for j, (category, count) in enumerate(sorted_abstracted_states[:3]):  # Only show top 3 states
                state_breakdown += f"""
                                <div style="background: #f8f9fa; border-radius: 6px; border: 1px solid #e9ecef; padding: 8px 12px; margin-bottom: 8px; text-align: left;">
                                    <span style="font-size: 12px; color: #555; font-weight: 500; float: left;">{category}</span>
                                    <span style="font-size: 14px; font-weight: 700; color: #0078d4; background: white; padding: 4px 8px; border-radius: 4px; min-width: 25px; text-align: center; border: 1px solid #dee2e6; float: right;">{count}</span>
                                    <div style="clear: both;"></div>
                                </div>"""
            
            html_content += f"""
                    <td style="width: 25%; padding: 0; text-align: center; vertical-align: top;">
                        <div style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 4px solid #0078d4; min-height: 120px;">
                            <div style="font-size: 16px; font-weight: 600; color: #333; margin-bottom: 10px; text-align: center;">{engineer}</div>
                            <div style="color: #0078d4; font-weight: 500; margin-bottom: 10px; text-align: center; font-size: 13px;">[ITEMS] {total_items} items</div>
                            <div style="margin-top: 10px;">
                                {state_breakdown}
                            </div>
                        </div>
                    </td>"""
        
        # Fill remaining cells in first row if less than 4 engineers
        for i in range(len(engineer_list), 4):
            html_content += '<td style="width: 25%; padding: 0;"></td>'
        
        html_content += "</tr>"
        
        # Second row (remaining engineers, if any)
        if len(engineer_list) > 4:
            html_content += "<tr>"
            for i in range(4, min(8, len(engineer_list))):
                engineer, metrics = engineer_list[i]
                total_items = metrics.get('total_items', 0)
                states = metrics.get('states', {})
                
                # Generate state breakdown with abstraction mapping
                abstracted_engineer_states = {}
                for state, count in states.items():
                    category = Config.get_state_category(state)
                    abstracted_engineer_states[category] = abstracted_engineer_states.get(category, 0) + count
                
                # Sort abstracted states by count and show only top 3
                sorted_abstracted_states = sorted(abstracted_engineer_states.items(), key=lambda x: x[1], reverse=True)
                
                state_breakdown = ""
                for j, (category, count) in enumerate(sorted_abstracted_states[:3]):  # Only show top 3 states
                    state_breakdown += f"""
                                <div style="background: #f8f9fa; border-radius: 6px; border: 1px solid #e9ecef; padding: 8px 12px; margin-bottom: 8px; text-align: left;">
                                    <span style="font-size: 12px; color: #555; font-weight: 500; float: left;">{category}</span>
                                    <span style="font-size: 14px; font-weight: 700; color: #0078d4; background: white; padding: 4px 8px; border-radius: 4px; min-width: 25px; text-align: center; border: 1px solid #dee2e6; float: right;">{count}</span>
                                    <div style="clear: both;"></div>
                                </div>"""
                
                html_content += f"""
                    <td style="width: 25%; padding: 0; text-align: center; vertical-align: top;">
                        <div style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 4px solid #0078d4; min-height: 120px;">
                            <div style="font-size: 16px; font-weight: 600; color: #333; margin-bottom: 10px; text-align: center;">{engineer}</div>
                            <div style="color: #0078d4; font-weight: 500; margin-bottom: 10px; text-align: center; font-size: 13px;">[ITEMS] {total_items} items</div>
                            <div style="margin-top: 10px;">
                                {state_breakdown}
                            </div>
                        </div>
                    </td>"""
            
            # Fill remaining cells in second row if less than 8 engineers
            for i in range(len(engineer_list), 8):
                html_content += '<td style="width: 25%; padding: 0;"></td>'
            
            html_content += "</tr>"
        
        html_content += """
                </table>
            </div>
        </div>
"""
    
    # Add footer
    html_content += f"""
        <div style="background: #f8f9fa; padding: 15px 20px; text-align: center; color: #666; font-size: 12px;">
            <p style="margin: 0;">Generated by <span style="color: #0078d4; font-weight: 600;">Azure DevOps AI Agent</span> | 
            Sprint Period: <span style="color: #0078d4; font-weight: 600;">{sprint_start}</span> to <span style="color: #0078d4; font-weight: 600;">{sprint_end}</span></p>
        </div>
    </div>
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
