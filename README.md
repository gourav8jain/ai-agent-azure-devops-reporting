# Azure DevOps AI Agent - Sprint Reporting System

🚀 **Automated Sprint Progress Tracking and Email Reporting for Azure DevOps**

A comprehensive AI-powered reporting system that automatically extracts sprint data from Azure DevOps, generates professional HTML reports, and delivers them via email with perfect rendering across all email clients.

## ✨ Features

### 📊 **Data Extraction**
- **Real-time Azure DevOps Integration**: Connects directly to Azure DevOps REST API
- **Sprint Discovery**: Automatically identifies current and relevant sprints
- **Work Item Analysis**: Extracts work items with status, assignee, and progress tracking
- **Multi-Project Support**: Handles multiple Azure DevOps projects simultaneously
- **Tag-based Filtering**: Supports filtering by specific tags (e.g., "HRMS - Payout")

### 🎨 **Report Generation**
- **Professional HTML Reports**: Clean, modern design with Azure DevOps branding
- **Status Abstraction**: Maps work item states to business-friendly categories:
  - `To-Do`: Open, TO DO, New, REQ-Review
  - `In Progress`: In Progress, Code Review
  - `In QA`: On-QA, Fixed
  - `Release Pending`: QA Reviewed, SIGNOFF
  - `Released`: DONE, Done, Closed, Resolved, Completed
  - `Drop`: Drop
- **Engineer Breakdown**: Individual engineer performance metrics
- **Status Summary**: Project-level status overview
- **Compact Layout**: Optimized for 2-page email viewing

### 📧 **Email Delivery**
- **Email-Optimized HTML**: Inline styles for perfect email client rendering
- **Cross-Platform Compatibility**: Works with Gmail, Outlook, Apple Mail, etc.
- **Automated Sending**: Direct SMTP integration with Gmail
- **Professional Formatting**: Consistent appearance across all email platforms

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Azure DevOps    │    │ AI Agent         │    │ Email Delivery │
│ REST API        │───▶│ Data Processing  │───▶│ SMTP Server    │
│                 │    │ & Report Gen     │    │ (Gmail)        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │ HTML Reports     │
                       │ (Email & Web)    │
                       └──────────────────┘
```

## 📋 Prerequisites

- **Python 3.9+**
- **Azure DevOps Organization** with Personal Access Token (PAT)
- **Gmail Account** with App Password (for email sending)
- **Git** (for version control)

## 🚀 Quick Start

### 1. **Clone the Repository**
```bash
git clone https://github.com/gourav8jain/ai-agent-azure-devops-reporting.git
cd ai-agent-azure-devops-reporting
```

### 2. **Set Up Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. **Configure Environment Variables**
```bash
cp env.example .env
# Edit .env with your credentials
```

### 4. **Run the Complete Workflow**
```bash
# Extract sprint data
python3 get_sprint_count.py

# Generate compact HTML report
python3 generate_html_report_compact.py

# Send report via email
python3 send_email_direct.py
```

## ⚙️ Configuration

### **Environment Variables (.env)**
```bash
# Azure DevOps Configuration
AZURE_DEVOPS_ORG=your_organization_name
AZURE_DEVOPS_PAT=your_personal_access_token

# Email Configuration
EMAIL_FROM=your_email@gmail.com
EMAIL_TO=recipient_email@gmail.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
```

### **Project Configuration (config.py)**
```python
# Sprint Period
SPRINT_PERIOD = {
    'start_date': '19-Aug-2025',
    'end_date': '01-Sep-2025'
}

# Project Settings
PROJECTS = {
    'NEWTON': {
        'tags': ['HRMS - Payout'],
        'iteration_path': 'NEWTON\\NEWTON Q2 19-Aug-2025 - 01-Sep-2025'
    },
    'Partner Management Tool': {
        'tags': [],
        'iteration_path': 'Partner Management Tool\\PMT Q2 19-Aug-2025 - 01-Sep-2025'
    }
}
```

## 📁 Project Structure

```
ai-agent-azure-devops-reporting/
├── 📊 Core Scripts
│   ├── get_sprint_count.py              # Sprint data extraction
│   ├── generate_html_report_compact.py  # Compact HTML report generation
│   └── send_email_direct.py             # Email delivery
├── ⚙️ Configuration
│   ├── config.py                        # Main configuration
│   ├── .env                             # Environment variables
│   └── env.example                      # Environment template
├── 📋 Documentation
│   ├── README.md                        # This file
│   └── quick_start.sh                   # Quick start script
├── 📦 Dependencies
│   ├── requirements.txt                  # Python packages
│   └── .gitignore                       # Git ignore rules
└── 📁 Data & Output
    ├── data/                            # Data storage
    └── venv/                            # Virtual environment
```

## 🔧 Usage Examples

### **Generate and Send Daily Report**
```bash
# Complete workflow in one go
./quick_start.sh
```

### **Custom Sprint Period**
```python
# Modify config.py
SPRINT_PERIOD = {
    'start_date': '01-Sep-2025',
    'end_date': '15-Sep-2025'
}
```

### **Add New Project**
```python
# Add to config.py PROJECTS
'New Project': {
    'tags': ['Custom Tag'],
    'iteration_path': 'Project\\Sprint Path'
}
```

## 📊 Report Features

### **Summary Cards**
- Total Work Items count
- Number of active projects
- Total engineers involved

### **Project Sections**
- Project-specific status breakdown
- Tag filtering information
- Iteration path details

### **Status Summary**
- Work items by status category
- Visual status distribution
- Count-based prioritization

### **Engineer Breakdown**
- Individual engineer metrics
- Work item distribution by status
- Performance overview (2x4 grid layout)

## 🎯 Email Optimization

### **Inline Styles**
- All CSS properties embedded in HTML
- No external stylesheet dependencies
- Consistent rendering across email clients

### **Compact Layout**
- Reduced spacing and padding
- Optimized for 2-page viewing
- Professional appearance maintained

### **Cross-Platform Support**
- Gmail (web and mobile)
- Outlook (desktop and web)
- Apple Mail
- Thunderbird
- Mobile email apps

## 🔒 Security Features

- **Environment Variables**: No hardcoded credentials
- **Personal Access Tokens**: Secure Azure DevOps authentication
- **Gmail App Passwords**: Enhanced email security
- **Git Ignore**: Sensitive files excluded from version control

## 🚀 Advanced Features

### **Automatic Sprint Discovery**
- Date-based sprint identification
- Configurable date ranges
- Include/exclude project filtering

### **State Categorization**
- Customizable status mapping
- Business-friendly terminology
- Flexible category definitions

### **Multi-Format Output**
- HTML reports for email
- JSON data for API integration
- Structured data for analysis

## 🐛 Troubleshooting

### **Common Issues**

#### **Email Not Sending**
```bash
# Check environment variables
cat .env

# Verify Gmail App Password
# Enable 2-Step Verification and generate App Password
```

#### **Azure DevOps Connection Issues**
```bash
# Verify PAT permissions
# Check organization name
# Ensure project access
```

#### **HTML Rendering Problems**
```bash
# Use compact HTML generator
python3 generate_html_report_compact.py

# Check email client compatibility
```

### **Debug Mode**
```python
# Enable debug logging in config.py
DEBUG_MODE = True
```

## 📈 Performance

- **Data Extraction**: ~5-10 seconds for typical sprints
- **Report Generation**: ~2-3 seconds
- **Email Delivery**: ~3-5 seconds
- **Total Workflow**: ~10-20 seconds

## 🔄 Automation

### **Cron Jobs (Linux/Mac)**
```bash
# Daily at 9:00 AM
0 9 * * * cd /path/to/project && ./quick_start.sh
```

### **Task Scheduler (Windows)**
- Create scheduled task
- Run `quick_start.sh` or individual scripts
- Configure for daily/weekly execution

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature-name`
3. **Make changes and test**
4. **Commit changes**: `git commit -m 'Add feature'`
5. **Push to branch**: `git push origin feature-name`
6. **Create Pull Request**

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### **Documentation**
- This README file
- Inline code comments
- Configuration examples

### **Issues**
- GitHub Issues: [Report a Bug](https://github.com/gourav8jain/ai-agent-azure-devops-reporting/issues)
- Feature Requests: [Request Feature](https://github.com/gourav8jain/ai-agent-azure-devops-reporting/issues)

### **Contact**
- **Developer**: Gourav Jain
- **Email**: gourav.jain@delhivery.com
- **Organization**: Delhivery

## 🎉 Acknowledgments

- **Azure DevOps Team**: For excellent REST API
- **Gmail Team**: For reliable SMTP service
- **Open Source Community**: For Python packages and tools

---

**Made with ❤️ for efficient sprint reporting and team collaboration**

*Last updated: August 29, 2025*
