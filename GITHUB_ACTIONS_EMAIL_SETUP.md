# 📧 GitHub Actions Email Configuration

This document explains how to configure multiple email recipients in GitHub Actions for the Azure DevOps Sprint Report.

## 🔧 Setting Up EMAIL_TO_MULTIPLE Secret

### Step 1: Go to Repository Secrets
1. Navigate to your GitHub repository
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

### Step 2: Add EMAIL_TO_MULTIPLE Secret
1. **Name**: `EMAIL_TO_MULTIPLE`
2. **Value**: `email1@company.com,email2@company.com,email3@company.com`
   - Use comma-separated email addresses
   - No spaces around commas
   - Maximum recommended: 50 recipients

### Step 3: Example Configurations

#### Multiple Team Members
```
EMAIL_TO_MULTIPLE=gourav.jain@iol.world,tech.lead@company.com,product.manager@company.com,qa.lead@company.com
```

#### Management Reporting
```
EMAIL_TO_MULTIPLE=gourav.jain@iol.world,cto@company.com,engineering.manager@company.com
```

#### Project-Specific Teams
```
# For IOL Pay team
EMAIL_TO_MULTIPLE=gourav.jain@iol.world,iol.pay.team@company.com,iol.pay.manager@company.com

# For VCC team
EMAIL_TO_MULTIPLE=gourav.jain@iol.world,vcc.team@company.com,vcc.manager@company.com
```

## 🔄 How It Works

### Priority Order
1. **EMAIL_TO_MULTIPLE** (if set) → Multiple recipients
2. **EMAIL_TO** (if EMAIL_TO_MULTIPLE is not set) → Single recipient
3. **Default** → gourav.jain@iol.world

### Workflow Behavior
- If `EMAIL_TO_MULTIPLE` is set, it will be used for all recipients
- If `EMAIL_TO_MULTIPLE` is empty/not set, `EMAIL_TO` will be used
- The workflow will show which configuration is being used

## 📋 Required Secrets

Make sure these secrets are configured in your repository:

### Required Secrets
- `AZURE_DEVOPS_PAT` - Your Azure DevOps Personal Access Token
- `EMAIL_FROM` - Sender email address
- `SMTP_USERNAME` - Gmail username
- `SMTP_PASSWORD` - Gmail App Password

### Optional Secrets
- `EMAIL_TO` - Single recipient (fallback)
- `EMAIL_TO_MULTIPLE` - Multiple recipients (comma-separated)

## 🚀 Testing the Configuration

### Manual Workflow Trigger
1. Go to **Actions** tab in your repository
2. Select **Daily Sprint Report** workflow
3. Click **Run workflow**
4. Check the logs for email recipient information

### Debug Information
The workflow will show:
- Which email configuration is being used
- List of recipients
- Count of recipients
- Environment variable status

## 🔍 Troubleshooting

### Common Issues

#### 1. EMAIL_TO_MULTIPLE Not Working
- **Check**: Secret is named exactly `EMAIL_TO_MULTIPLE`
- **Check**: No spaces around commas in the value
- **Check**: Secret is set in the correct repository

#### 2. No Emails Received
- **Check**: Spam folder
- **Check**: Gmail App Password is correct
- **Check**: Email addresses are valid

#### 3. Authentication Failed
- **Check**: Gmail App Password (not regular password)
- **Check**: 2-Step Verification is enabled
- **Check**: SMTP_USERNAME and SMTP_PASSWORD secrets

### Debug Steps
1. Check workflow logs for "Show Email Recipients" step
2. Verify environment variables are set correctly
3. Test with a single email first, then add multiple

## 📊 Current Sprint Configuration

The system is configured for:
- **IOL Pay**: Iteration-28 (Oct 14 - Nov 3)
- **VCC**: Sprint-11 (Oct 14 - Oct 27)
- **Status Categories**: To Do, In Progress, Ready for QA, QA in Progress, Ready for Release, Done

## 🎯 Example Workflow Logs

When EMAIL_TO_MULTIPLE is configured correctly, you'll see:
```
📧 Email Recipients Configuration:
   Recipients: ['gourav.jain@iol.world', 'manager@company.com', 'team@company.com']
   Count: 3
   Using EMAIL_TO_MULTIPLE: gourav.jain@iol.world,manager@company.com,team@company.com
```

## 🔒 Security Notes

- Email addresses in secrets are encrypted
- Use comma-separated format (no spaces)
- Maximum recommended: 50 recipients per email
- Gmail has daily sending limits (500 emails/day for free accounts)

## 📞 Support

If you encounter issues:
1. Check the workflow logs for detailed error messages
2. Verify all required secrets are set
3. Test with a single email first
4. Check Gmail App Password configuration
