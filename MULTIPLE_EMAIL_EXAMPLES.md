# 📧 Multiple Email Recipients Configuration

This document explains how to configure the Azure DevOps Sprint Report system to send emails to multiple recipients.

## 🎯 Configuration Options

### Option 1: Environment Variables (Recommended)

#### Single Recipient (Default)
```bash
export AZURE_DEVOPS_PAT='your_azure_devops_pat_here'
export EMAIL_TO='gourav.jain@iol.world'
python3 run_complete_workflow_updated.py
```

#### Multiple Recipients
```bash
export AZURE_DEVOPS_PAT='your_azure_devops_pat_here'
export EMAIL_TO_MULTIPLE='gourav.jain@iol.world,manager@company.com,team@company.com'
python3 run_complete_workflow_updated.py
```

### Option 2: Using Scripts

#### Single Recipient
```bash
export AZURE_DEVOPS_PAT='your_azure_devops_pat_here'
./send_report_to_iol.sh
```

#### Multiple Recipients
```bash
export AZURE_DEVOPS_PAT='your_azure_devops_pat_here'
export EMAIL_TO_MULTIPLE='gourav.jain@iol.world,manager@company.com,team@company.com'
./send_to_multiple_emails.sh
```

## 📋 Email Configuration Examples

### Example 1: Team Distribution
```bash
export EMAIL_TO_MULTIPLE='gourav.jain@iol.world,tech.lead@company.com,product.manager@company.com,qa.lead@company.com'
```

### Example 2: Management Reporting
```bash
export EMAIL_TO_MULTIPLE='gourav.jain@iol.world,cto@company.com,engineering.manager@company.com'
```

### Example 3: Project-Specific Teams
```bash
# For IOL Pay team
export EMAIL_TO_MULTIPLE='gourav.jain@iol.world,iol.pay.team@company.com,iol.pay.manager@company.com'

# For VCC team  
export EMAIL_TO_MULTIPLE='gourav.jain@iol.world,vcc.team@company.com,vcc.manager@company.com'
```

### Example 4: Cross-Organization Reporting
```bash
export EMAIL_TO_MULTIPLE='gourav.jain@iol.world,iwtx.manager@company.com,iolpulse.manager@company.com'
```

## 🔧 Configuration Priority

The system follows this priority order:

1. **EMAIL_TO_MULTIPLE** (if set) - Multiple recipients
2. **EMAIL_TO** (if EMAIL_TO_MULTIPLE is not set) - Single recipient
3. **Default** - gourav.jain@iol.world

## 📊 Current Sprint Configuration

The system is configured for:
- **IOL Pay**: Iteration-28 (Oct 14 - Nov 3)
- **VCC**: Sprint-11 (Oct 14 - Oct 27)
- **Status Categories**: To Do, In Progress, Ready for QA, QA in Progress, Ready for Release, Done

## 🚀 Quick Start Examples

### Send to IOL Team
```bash
export AZURE_DEVOPS_PAT='your_pat_here'
export EMAIL_TO_MULTIPLE='gourav.jain@iol.world,iol.team@company.com'
./send_to_multiple_emails.sh
```

### Send to Management
```bash
export AZURE_DEVOPS_PAT='your_pat_here'
export EMAIL_TO_MULTIPLE='gourav.jain@iol.world,cto@company.com,engineering.manager@company.com'
./send_to_multiple_emails.sh
```

### Send to All Stakeholders
```bash
export AZURE_DEVOPS_PAT='your_pat_here'
export EMAIL_TO_MULTIPLE='gourav.jain@iol.world,tech.lead@company.com,product.manager@company.com,qa.lead@company.com,engineering.manager@company.com'
./send_to_multiple_emails.sh
```

## 📧 Email Format

All recipients will receive:
- Professional HTML report optimized for email
- Current sprint data only (Oct 14 - Oct 27)
- IOL Pay and VCC project data
- Engineer breakdown and status summary
- Mobile-friendly format

## 🔒 Security Notes

- Email addresses are case-insensitive
- Invalid email addresses will be filtered out
- Maximum recommended: 50 recipients per email
- Gmail has sending limits (500 emails/day for free accounts)

## 🐛 Troubleshooting

### Common Issues

1. **No emails received**: Check spam folder
2. **Authentication failed**: Verify Gmail App Password
3. **Invalid recipients**: Check email format (no spaces around commas)
4. **Rate limiting**: Gmail has daily sending limits

### Debug Mode
```bash
export DEBUG_EMAIL=true
./send_to_multiple_emails.sh
```

## 📞 Support

For issues with multiple email configuration, check:
1. Email format (comma-separated, no spaces)
2. Gmail App Password configuration
3. Azure DevOps PAT permissions
4. Network connectivity
