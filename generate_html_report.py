import json
import os
from datetime import datetime
from config import Config

def generate_html_report(sprint_data_file):
    """Generate HTML report from sprint data"""
    
    # Load sprint data
    try:
        with open(sprint_data_file, 'r', encoding='utf-8') as f:
            sprint_data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading sprint data: {str(e)}")
        return None
    
    # Generate HTML content
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Azure DevOps Sprint Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #0078d4 0%, #106ebe 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 16px;
        }}
        .summary-cards {{
            padding: 30px;
            background: #f8f9fa;
        }}
        .summary-cards table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
        }}
        .summary-cards td {{
            padding: 20px;
            text-align: center;
            vertical-align: top;
        }}
        .card {{
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-left: 5px solid #0078d4;
            height: 100%;
            min-height: 120px;
        }}
        .card h3 {{
            margin: 0 0 15px 0;
            color: #0078d4;
            font-size: 20px;
            font-weight: 600;
        }}
        .card .count {{
            font-size: 36px;
            font-weight: 700;
            color: #333;
            margin: 10px 0;
        }}
        .card .meta {{
            color: #666;
            font-size: 14px;
            margin-top: 10px;
        }}
        .project-section {{
            padding: 30px;
            border-bottom: 1px solid #e9ecef;
        }}
        .project-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #e9ecef;
        }}
        .project-header h2 {{
            margin: 0;
            color: #0078d4;
            font-size: 24px;
            font-weight: 600;
        }}
        .tag-filter {{
            background: #e3f2fd;
            color: #1976d2;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
        }}
        .iteration-path {{
            background: #f3e5f5;
            color: #7b1fa2;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 500;
            margin-top: 10px;
        }}
        .status-summary {{
            margin-bottom: 30px;
        }}
        .status-summary h3 {{
            color: #333;
            font-size: 20px;
            margin-bottom: 20px;
            font-weight: 600;
        }}
        .status-grid {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
        }}
        .status-grid td {{
            padding: 15px;
            text-align: center;
            vertical-align: top;
        }}
        .status-item {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-left: 4px solid #0078d4;
            height: 100%;
            min-height: 80px;
        }}
        .status-name {{
            font-size: 16px;
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
            display: block;
        }}
        .status-count {{
            font-size: 24px;
            font-weight: 700;
            color: #0078d4;
            display: block;
        }}
        .engineer-section {{
            padding: 30px;
        }}
        .engineer-section h3 {{
            color: #333;
            font-size: 20px;
            margin-bottom: 25px;
            font-weight: 600;
        }}
        .engineer-grid {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
        }}
        .engineer-grid td {{
            padding: 15px;
            text-align: left;
            vertical-align: top;
        }}
        .engineer-card {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-left: 5px solid #0078d4;
            height: 100%;
            min-height: 120px;
            display: flex;
            flex-direction: column;
        }}
        .engineer-name {{
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 15px;
            text-align: left;
        }}
        .state-breakdown {{
            flex-grow: 1;
        }}
        .state-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
            padding: 8px 12px;
            background: #f8f9fa;
            border-radius: 6px;
        }}
        .state-name {{
            font-size: 14px;
            color: #555;
            font-weight: 500;
        }}
        .state-count {{
            font-size: 16px;
            font-weight: 700;
            color: #0078d4;
            background: white;
            padding: 4px 8px;
            border-radius: 4px;
            min-width: 30px;
            text-align: center;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px 30px;
            text-align: center;
            color: #666;
            font-size: 14px;
        }}
        .highlight {{
            color: #0078d4;
            font-weight: 600;
        }}
        @media print {{
            body {{ background: white; }}
            .container {{ box-shadow: none; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Azure DevOps Sprint Report</h1>
            <p>Sprint Period: {Config.SPRINT_PERIOD['start_date']} to {Config.SPRINT_PERIOD['end_date']}</p>
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <div class="summary-cards">
            <table>
                <tr>
                    <td>
                        <div class="card">
                            <h3>📊 Total Work Items</h3>
                            <div class="count">{sum(result['total_items'] for result in sprint_data.values())}</div>
                            <div class="meta">Across all projects</div>
                        </div>
                    </td>
                    <td>
                        <div class="card">
                            <h3>🏢 Projects</h3>
                            <div class="count">{len(sprint_data)}</div>
                            <div class="meta">Active projects in sprint</div>
                        </div>
                    </td>
                    <td>
                        <div class="card">
                            <h3>👥 Engineers</h3>
                            <div class="count">{sum(len(result['engineer_metrics']) for result in sprint_data.values())}</div>
                            <div class="meta">Team members involved</div>
                        </div>
                    </td>
                </tr>
            </table>
        </div>
"""
    
    # Add project sections
    for project_name, result in sprint_data.items():
        project_config = Config.get_project_config(project_name)
        
        # Get tag info
        tags = project_config['tags'] if project_config else []
        tag_display = f"Filtered by: {', '.join(tags)}" if tags else "All work items"
        
        # Get iteration path
        iteration_path = project_config['iteration_path'] if project_config else "Default iteration"
        
        # Calculate status-level summary using abstraction mapping
        status_summary = {}
        for engineer, metrics in result['engineer_metrics'].items():
            for state, count in metrics['states'].items():
                category = Config.get_state_category(state)
                status_summary[category] = status_summary.get(category, 0) + count
        
        html_content += f"""
        <div class="project-section">
            <div class="project-header">
                <h2>{project_name}</h2>
                <div class="tag-filter">{tag_display}</div>
            </div>
            <div class="iteration-path">📅 Iteration: {iteration_path}</div>
            
            <div class="status-summary">
                <h3>📈 Status Level Summary</h3>
                <table class="status-grid">
                    <tr>
"""
        
        # Generate status summary cards
        status_items = list(status_summary.items())
        for i, (status, count) in enumerate(status_items):
            if i > 0 and i % 3 == 0:
                html_content += "</tr><tr>"
            html_content += f"""
                        <td>
                            <div class="status-item">
                                <span class="status-name">{status}</span>
                                <span class="status-count">{count}</span>
                            </div>
                        </td>"""
        
        # Fill remaining cells if needed
        remaining_cells = 3 - (len(status_items) % 3)
        if remaining_cells < 3:
            for _ in range(remaining_cells):
                html_content += "<td></td>"
        
        html_content += """
                    </tr>
                </table>
            </div>
            
            <div class="engineer-section">
                <h3>👨‍💻 Engineer Level Breakdown</h3>
                <table class="engineer-grid">
"""
        
        # Generate engineer cards in two rows
        engineer_cards = ""
        engineer_list = list(result['engineer_metrics'].items())
        
        # First row (first 4 engineers)
        engineer_cards += "<tr>"
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
                        <div class="state-item">
                            <span class="state-name">{category}</span>
                            <span class="state-count">{count}</span>
                        </div>"""
            
            engineer_cards += f"""
                    <td>
                        <div class="engineer-card">
                            <div class="engineer-name">{engineer}</div>
                            <div class="meta" style="color: #0078d4; font-weight: 500; margin-bottom: 12px; text-align: left;">📊 {total_items} items</div>
                            <div class="state-breakdown">
                                {state_breakdown}
                            </div>
                        </div>
                    </td>"""
        
        # Fill remaining cells in first row if less than 4 engineers
        for i in range(len(engineer_list), 4):
            engineer_cards += "<td></td>"
        
        engineer_cards += "</tr>"
        
        # Second row (remaining engineers, if any)
        if len(engineer_list) > 4:
            engineer_cards += "<tr>"
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
                        <div class="state-item">
                            <span class="state-name">{category}</span>
                            <span class="state-count">{count}</span>
                        </div>"""
                
                engineer_cards += f"""
                    <td>
                        <div class="engineer-card">
                            <div class="engineer-name">{engineer}</div>
                            <div class="meta" style="color: #0078d4; font-weight: 500; margin-bottom: 12px; text-align: left;">📊 {total_items} items</div>
                            <div class="state-breakdown">
                                {state_breakdown}
                            </div>
                        </div>
                    </td>"""
            
            # Fill remaining cells in second row if less than 8 engineers
            for i in range(len(engineer_list), 8):
                engineer_cards += "<td></td>"
            
            engineer_cards += "</tr>"
        
        html_content += engineer_cards + """
                </table>
            </div>
        </div>
"""
    
    # Add footer
    html_content += f"""
        <div class="footer">
            <p>Generated by <span class="highlight">Azure DevOps AI Agent</span> | 
            Sprint Period: <span class="highlight">{Config.SPRINT_PERIOD['start_date']}</span> to <span class="highlight">{Config.SPRINT_PERIOD['end_date']}</span></p>
        </div>
    </div>
</body>
</html>"""
    
    return html_content

def main():
    """Main function to generate HTML report"""
    print("🎨 HTML Report Generator")
    print("=" * 30)
    
    # Find the most recent sprint count file
    json_files = [f for f in os.listdir('.') if f.startswith('sprint_count_') and f.endswith('.json')]
    if not json_files:
        print("❌ No sprint count files found. Run get_sprint_count.py first.")
        return
    
    latest_file = max(json_files, key=lambda x: os.path.getctime(x))
    print(f"📁 Using data from: {latest_file}")
    
    # Generate HTML report
    html_content = generate_html_report(latest_file)
    
    if html_content:
        # Save HTML report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'sprint_report_{timestamp}.html'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML report generated: {output_file}")
        print(f"📊 Report size: {len(html_content)} characters")
        print(f"🌐 Open {output_file} in your browser to view the report")
        print(f"📧 Ready to send via email!")
    else:
        print("❌ Failed to generate HTML report")

if __name__ == "__main__":
    main()
