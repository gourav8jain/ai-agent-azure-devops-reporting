# 🔐 GitHub Repository Secrets Setup Guide

## 📋 **Required Secrets for Azure DevOps AI Agent**

This application requires the following secrets to be configured in your GitHub repository for GitHub Actions to work properly.

## 🚀 **Step-by-Step Setup**

### **1. Access Repository Settings**
1. Go to your GitHub repository: `https://github.com/gourav8jain/ai-agent-azure-devops-reporting`
2. Click on **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**

### **2. Add Required Secrets**
Click **New repository secret** and add each of these secrets:

#### **🔑 Azure DevOps Secrets**
| Secret Name | Value | Description |
|-------------|-------|-------------|
| `AZURE_DEVOPS_ORG` | `delhivery` | Your Azure DevOps organization name |
| `AZURE_DEVOPS_PAT` | `YOUR_AZURE_DEVOPS_PAT_HERE` | Your Azure DevOps Personal Access Token |

#### **📧 Email Configuration Secrets**
| Secret Name | Value | Description |
|-------------|-------|-------------|
| `EMAIL_FROM` | `your_email@gmail.com` | Sender email address |
| `EMAIL_TO` | `recipient_email@gmail.com` | Recipient email address |
| `SMTP_USERNAME` | `your_email@gmail.com` | Gmail username |
| `SMTP_PASSWORD` | `YOUR_GMAIL_APP_PASSWORD_HERE` | Gmail App Password |

### **3. Secret Values to Copy-Paste**

#### **Azure DevOps Configuration:**
```
AZURE_DEVOPS_ORG: delhivery
AZURE_DEVOPS_PAT: YOUR_AZURE_DEVOPS_PAT_HERE
```

#### **Email Configuration:**
```
EMAIL_FROM: your_email@gmail.com
EMAIL_TO: recipient_email@gmail.com
SMTP_USERNAME: your_email@gmail.com
SMTP_PASSWORD: YOUR_GMAIL_APP_PASSWORD_HERE
```

## 🔒 **Security Notes**

- **Never commit secrets to your code**
- **Secrets are encrypted and only visible to repository administrators**
- **Secrets are automatically available to GitHub Actions workflows**
- **Local development can still use .env files if needed**

## 🧪 **Testing the Setup**

### **1. Manual Workflow Trigger**
1. Go to **Actions** tab
2. Click **Daily Sprint Report**
3. Click **Run workflow**
4. Select **main** branch
5. Click **Run workflow**

### **2. Check Workflow Execution**
- Monitor the workflow execution in real-time
- Look for any error messages
- Verify that all secrets are being read correctly

## 🚨 **Troubleshooting**

### **Common Issues:**

#### **"Missing required environment variables"**
- Ensure all 6 secrets are added
- Check secret names are exactly as shown (case-sensitive)
- Verify secrets are added to the correct repository

#### **"Authentication failed"**
- Check Azure DevOps PAT is valid and not expired
- Verify Gmail App Password is correct
- Ensure 2-factor authentication is enabled on Gmail

#### **"Workflow not running automatically"**
- Check if repository has recent activity
- Verify workflow file is in `.github/workflows/` directory
- Check Actions permissions in repository settings

## 📅 **Workflow Schedule**

The workflow is configured to run:
- **Daily at 5:00 PM IST** (11:30 AM UTC)
- **Daily at 6:00 PM IST** (12:30 PM UTC) - Backup time
- **On every push to main branch** - For testing
- **Manually** - Via "Run workflow" button

## 🔄 **Updating Secrets**

To update any secret:
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Find the secret you want to update
3. Click the **Update** button
4. Enter the new value
5. Click **Update secret**

## 📚 **Additional Resources**

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Azure DevOps PAT Guide](https://docs.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens)
- [Gmail App Passwords](https://support.google.com/accounts/answer/185833)

## ✅ **Verification Checklist**

- [ ] All 6 secrets added to repository
- [ ] Secret names match exactly (case-sensitive)
- [ ] Workflow file exists in `.github/workflows/`
- [ ] Manual workflow trigger works
- [ ] No error messages in workflow logs
- [ ] Email received successfully
- [ ] Azure DevOps data extracted correctly

---

**Need help?** Check the workflow logs in the Actions tab for detailed error messages.
