#!/usr/bin/env python3
"""
Complete Azure DevOps Sprint Reporting Workflow
Automatically handles: data extraction, HTML generation, and email delivery
"""

import os
import json
from datetime import datetime
from config import Config
from get_sprint_count import main as extract_data
from generate_html_report_compact import generate_compact_html_report
from send_email_direct import send_email_directly

def check_csv_data_format(json_file):
    """Check if data follows the expected format"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Expected format: organization_project: {total_items, engineer_metrics}
        required_keys = ['total_items', 'engineer_metrics']
        
        for key, value in data.items():
            if not isinstance(value, dict):
                return False, f"Unexpected data structure for {key}"
            
            for req_key in required_keys:
                if req_key not in value:
                    return False, f"Missing '{req_key}' in {key}"
            
            if not isinstance(value['engineer_metrics'], dict):
                return False, f"'engineer_metrics' should be dict in {key}"
        
        return True, "Data format validation passed"
    
    except Exception as e:
        return False, f"Error reading JSON: {str(e)}"

def find_latest_json_file():
    """Find the most recent sprint count json file"""
    # Check data directory first
    data_dir = 'data'
    json_files = []
    
    if os.path.exists(data_dir):
        json_files = [f for f in os.listdir(data_dir) if f.startswith('sprint_count_') and f.endswith('.json')]
        json_files = [os.path.join(data_dir, f) for f in json_files]
    
    # Also check current directory for backward compatibility
    current_files = [f for f in os.listdir('.') if f.startswith('sprint_count_') and f.endswith('.json')]
    json_files.extend(current_files)
    
    if not json_files:
        return None, "No sprint count files found"
    
    # Sort by modification time and return the latest
    latest_file = max(json_files, key=lambda x: os.path.getctime(x))
    return latest_file, f"Using file: {latest_file}"

def main():
    """Complete workflow for Azure DevOps sprint reporting"""
    print("🚀 Complete Azure DevOps Sprint Reporting Workflow")
    print("=" * 60)
    print()
    
    # Step 1: Validate Configuration
    print("🔧 Step 1: Validating Configuration...")
    if not Config.validate_config():
        print("❌ Configuration validation failed")
        return False
    
    print("✅ Configuration validated successfully")
    print()
    
    # Step 2: Extract Sprint Data
    print("📊 Step 2: Extracting Sprint Data from Azure DevOps...")
    try:
        extract_data()
        print("✅ Sprint data extracted successfully")
    except Exception as e:
        print(f"❌ Failed to extract sprint data: {str(e)}")
        return False
    
    print()
    
    # Step 3: Validate Extracted Data
    print("🔍 Step 3: Validating Extracted Data...")
    json_file, message = find_latest_json_file()
    if not json_file:
        print(f"❌ {message}")
        return False
    
    print(f"✅ {message}")
    
    # Validate data format
    is_valid, validation_message = check_csv_data_format(json_file)
    if not is_valid:
        print(f"❌ Data format validation failed: {validation_message}")
        return False
    
    print(f"✅ {validation_message}")
    print()
    
    # Step 4: Generate HTML Report
    print("🎨 Step 4: Generating HTML Report...")
    try:
        html_content = generate_compact_html_report(json_file)
        if not html_content:
            print("❌ HTML report generation failed")
            return False
        
        # Save HTML report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'compact_sprint_report_{timestamp}.html'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Compact HTML report generated: {output_file}")
        print(f"📊 Report size: {len(html_content)} characters")
        print("🌐 Open the HTML file in your browser to view the report")
        print("📧 Ready to send via email!")
        print()
        
        # Step 5: Send Email (Optional)
        email_choice = input("📧 Do you want to send the report via email? (y/n): ").lower().strip()
        if email_choice in ['y', 'yes']:
            print("📧 Step 5: Sending Email...")
            
            try:
                # Update email credentials if needed
                if not Config.SMTP_PASSWORD:
                    smtp_password = input("Enter your Gmail App Password for SMTP_PASSWORD: ").strip()
                    Config.SMTP_PASSWORD = smtp_password
                
                result = send_email_directly(output_file, html_content)
                if result:
                    print("✅ Email sent successfully!")
                else:
                    print("❌ Email sending failed")
                
            except KeyboardInterrupt:
                print("\n⏹️ Email sending cancelled by user")
            except Exception as e:
                print(f"❌ Email sending error: {str(e)}")
        else:
            print("📧 Email sending skipped")
        
        print()
        
        # Final Summary
        print("🎯 Workflow Summary:")
        print("✅ Configuration validated")
        print("✅ Sprint data extracted from Azure DevOps") 
        print("✅ HTML report generated")
        print("✅ Report ready for viewing/sending")
        print()
        print(f"📁 Generated files:")
        print(f"   📊 Data: {json_file}")
        print(f"   🎨 Report: {output_file}")
        print()
        print("🎉 Complete Azure DevOps Sprint Reporting Workflow Finished Successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ HTML report generation failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
