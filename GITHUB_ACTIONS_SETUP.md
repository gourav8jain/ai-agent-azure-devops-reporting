# 🚀 GitHub Actions Deployment Guide

## Overview
This guide explains how to deploy the Azure DevOps AI Agent using GitHub Actions to run automatically every day at 10:30 AM IST.

## ⚠️ Important Notes

### ❌ **GitHub Pages Limitation**
- **Cannot run Python applications**
- **Cannot execute scheduled jobs**
- **Cannot connect to external APIs**
- **Cannot send emails**

### ✅ **GitHub Actions Solution**
- **Runs Python applications**
- **Supports scheduled execution**
- **Can connect to Azure DevOps APIs**
- **Can send emails via SMTP**

## 🛠️ Setup Instructions

### 1. **Enable GitHub Actions**
1. Go to your repository on GitHub
2. Click on **Actions** tab
3. Click **Enable Actions** if not already enabled

### 2. **Set Up Repository Secrets**
Navigate to **Settings** → **Secrets and variables** → **Actions**

Add these secrets:

```bash
# Azure DevOps Configuration
AZURE_DEVOPS_ORG          # Your Azure DevOps organization name
AZURE_DEVOPS_PAT          # Your Personal Access Token

# Email Configuration
EMAIL_FROM                 # Sender email address
EMAIL_TO                   # Recipient email address
SMTP_USERNAME             # Gmail username
SMTP_PASSWORD             # Gmail App Password
```

### 3. **Workflow File Location**
The workflow file is already created at:
```
.github/workflows/daily-report.yml
```

### 4. **Schedule Configuration**
The workflow runs daily at **10:30 AM IST** (5:00 AM UTC):

```yaml
on:
  schedule:
    - cron: '0 5 * * *'  # 5:00 AM UTC = 10:30 AM IST
```

**Cron Format Explanation:**
- `0` - Minute (0-59)
- `5` - Hour (0-23) in UTC
- `*` - Day of month (1-31)
- `*` - Month (1-12)
- `*` - Day of week (0-6, Sunday=0)

### 5. **Manual Trigger**
You can also run the workflow manually:
1. Go to **Actions** tab
2. Click on **Daily Sprint Report**
3. Click **Run workflow** button

## 🔧 Customization Options

### **Change Schedule**
Modify the cron expression in `.github/workflows/daily-report.yml`:

```yaml
# Examples:
- cron: '0 5 * * *'      # Daily at 5:00 AM UTC (10:30 AM IST)
- cron: '0 5 * * 1-5'    # Weekdays only
- cron: '0 5 1 * *'      # First day of each month
- cron: '0 5 * * 1'      # Every Monday
```

### **Multiple Times Per Day**
```yaml
on:
  schedule:
    - cron: '0 5 * * *'      # 10:30 AM IST
    - cron: '0 17 * * *'     # 10:30 PM IST
```

### **Different Time Zones**
Convert your desired time to UTC:

| IST Time | UTC Time | Cron Expression |
|----------|----------|-----------------|
| 9:00 AM  | 3:30 AM  | `30 3 * * *`    |
| 10:30 AM | 5:00 AM  | `0 5 * * *`     |
| 2:00 PM  | 8:30 AM  | `30 8 * * *`    |
| 6:00 PM  | 12:30 PM | `30 12 * * *`   |

## 📊 Workflow Execution

### **What Happens Each Day:**
1. **5:00 AM UTC (10:30 AM IST)**: Workflow automatically starts
2. **Checkout**: Downloads latest code
3. **Setup**: Installs Python and dependencies
4. **Extract Data**: Connects to Azure DevOps and gets sprint data
5. **Generate Report**: Creates compact HTML report
6. **Send Email**: Delivers report via email
7. **Upload Artifacts**: Saves reports for 7 days
8. **Success Notification**: Logs completion status

### **Execution Time:**
- **Total Duration**: ~2-5 minutes
- **Data Extraction**: ~30 seconds
- **Report Generation**: ~10 seconds
- **Email Sending**: ~30 seconds

## 🔍 Monitoring and Debugging

### **View Workflow Runs**
1. Go to **Actions** tab
2. Click on **Daily Sprint Report**
3. View execution history and logs

### **Check Logs**
1. Click on any workflow run
2. Click on **generate-and-send-report** job
3. Expand individual steps to see logs

### **Common Issues**
- **Authentication Errors**: Check Azure DevOps PAT
- **Email Failures**: Verify Gmail App Password
- **Dependency Issues**: Check requirements.txt
- **Schedule Issues**: Verify cron expression

## 🚀 Advanced Features

### **Conditional Execution**
```yaml
- name: Check if it's a workday
  run: |
    if [[ $(date +%u) -gt 5 ]]; then
      echo "Weekend - skipping report"
      exit 1
    fi
```

### **Error Handling**
```yaml
- name: Send Report
  run: python3 send_email_direct.py
  continue-on-error: true
  
- name: Notify on Failure
  if: failure()
  run: |
    echo "Report generation failed!"
    # Add notification logic here
```

### **Multiple Recipients**
```yaml
- name: Send to Multiple Recipients
  run: |
    for email in ${{ secrets.EMAIL_LIST }}; do
      EMAIL_TO=$email python3 send_email_direct.py
    done
```

## 📱 Notifications

### **GitHub Notifications**
- Email notifications for workflow failures
- Repository activity updates
- Pull request and issue notifications

### **External Notifications**
Add webhook notifications to:
- Slack
- Microsoft Teams
- Discord
- Email lists

## 🔒 Security Considerations

### **Secret Management**
- Never commit secrets to code
- Use GitHub repository secrets
- Rotate PATs and passwords regularly
- Limit PAT permissions to minimum required

### **Access Control**
- Restrict workflow file access
- Review workflow permissions
- Monitor workflow execution logs

## 📈 Cost and Limits

### **GitHub Actions Limits**
- **Free Tier**: 2,000 minutes/month
- **Public Repos**: Unlimited minutes
- **Private Repos**: 2,000 minutes/month (free tier)

### **Our Workflow Usage**
- **Daily Execution**: ~5 minutes/day
- **Monthly Usage**: ~150 minutes/month
- **Cost**: Free (within limits)

## 🎯 Best Practices

1. **Test Locally First**: Ensure scripts work before deploying
2. **Monitor Execution**: Check logs regularly
3. **Handle Errors Gracefully**: Add error handling and notifications
4. **Keep Secrets Secure**: Never expose credentials
5. **Version Control**: Track workflow changes in git
6. **Documentation**: Keep setup guides updated

## 🆘 Troubleshooting

### **Workflow Not Running**
- Check GitHub Actions is enabled
- Verify cron syntax
- Check repository permissions
- Review workflow file syntax

### **Authentication Issues**
- Verify Azure DevOps PAT is valid
- Check organization name
- Ensure PAT has required permissions
- Test connection locally

### **Email Delivery Problems**
- Verify Gmail App Password
- Check 2-Step Verification is enabled
- Test SMTP connection locally
- Review email client settings

---

## 🎉 Success!

Once configured, your Azure DevOps AI Agent will:
- ✅ **Run automatically** every day at 10:30 AM IST
- ✅ **Generate reports** from Azure DevOps data
- ✅ **Send emails** with professional HTML reports
- ✅ **Store artifacts** for 7 days
- ✅ **Provide monitoring** and error handling

**No manual intervention required!** 🚀
