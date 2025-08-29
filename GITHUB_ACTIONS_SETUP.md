# 🚀 GitHub Actions Setup Guide

## 📋 **Complete Setup for Azure DevOps AI Agent**

This guide will help you set up GitHub Actions to run your Azure DevOps AI Agent automatically every day.

## 🔑 **Step 1: Add Repository Secrets**

### **Access Repository Settings:**
1. Go to your GitHub repository: `https://github.com/gourav8jain/ai-agent-azure-devops-reporting`
2. Click on **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**

### **Add These 6 Required Secrets:**

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `AZURE_DEVOPS_ORG` | `delhivery` | Your Azure DevOps organization name |
| `AZURE_DEVOPS_PAT` | `YOUR_AZURE_DEVOPS_PAT_HERE` | Your Azure DevOps Personal Access Token |
| `EMAIL_FROM` | `gourav8jain@gmail.com` | Sender email address |
| `EMAIL_TO` | `gourav8jain@gmail.com` | Recipient email address |
| `SMTP_USERNAME` | `gourav8jain@gmail.com` | Gmail username |
| `SMTP_PASSWORD` | `YOUR_GMAIL_APP_PASSWORD_HERE` | Gmail App Password |

### **How to Add Secrets:**
1. Click **New repository secret**
2. Enter the **Secret name** (exactly as shown above)
3. Enter the **Secret value**
4. Click **Add secret**
5. Repeat for all 6 secrets

## ⚙️ **Step 2: Verify Workflow File**

### **Check Workflow Location:**
The workflow file should be at: `.github/workflows/daily-report.yml`

### **Workflow Features:**
- **Schedule**: Daily at 5:00 PM IST (11:30 AM UTC)
- **Backup**: Daily at 6:00 PM IST (12:30 PM UTC)
- **Manual Trigger**: Click "Run workflow" anytime
- **Push Trigger**: Runs on every main branch push

## 🧪 **Step 3: Test the Setup**

### **Option 1: Manual Test (Recommended)**
1. Go to **Actions** tab in your repository
2. Click **Daily Sprint Report**
3. Click **Run workflow** button
4. Select **main** branch
5. Click **Run workflow**

### **Option 2: Push Test**
Make any small change to your code and push to main branch:
```bash
git add .
git commit -m "🧪 Test GitHub Actions workflow"
git push origin main
```

## 📅 **Step 4: Monitor Execution**

### **Check Workflow Status:**
1. Go to **Actions** tab
2. Click on **Daily Sprint Report**
3. Click on the latest run
4. Monitor each step in real-time

### **Expected Steps:**
1. ✅ **Checkout repository** - Downloads your code
2. ✅ **Set up Python** - Installs Python 3.9
3. ✅ **Install dependencies** - Installs required packages
4. ✅ **Debug Environment** - Shows environment info
5. ✅ **Validate Configuration** - Tests config setup
6. ✅ **Generate Sprint Report** - Extracts Azure DevOps data
7. ✅ **Generate HTML Report** - Creates email report
8. ✅ **Send Email Report** - Delivers via Gmail
9. ✅ **Upload Report Artifacts** - Saves reports
10. ✅ **Success Notification** - Confirms completion

## 🚨 **Troubleshooting Common Issues**

### **Issue: "Missing required environment variables"**
**Solution**: Ensure all 6 secrets are added correctly
- Check secret names are exactly as shown (case-sensitive)
- Verify secrets are added to the correct repository
- Ensure you're in the repository's **Settings** → **Secrets and variables** → **Actions**

### **Issue: "Authentication failed"**
**Solution**: Check credentials
- Verify Azure DevOps PAT is valid and not expired
- Check Gmail App Password is correct
- Ensure 2-factor authentication is enabled on Gmail

### **Issue: "Workflow not running automatically"**
**Solution**: Check workflow configuration
- Verify workflow file is in `.github/workflows/` directory
- Check Actions permissions in repository settings
- Ensure repository has recent activity

### **Issue: "Python dependencies failed"**
**Solution**: Check requirements.txt
- Verify all required packages are listed
- Check for any syntax errors in requirements.txt

## 🔍 **Debug Information**

### **Workflow Logs:**
Each step shows detailed information:
- Environment variables (masked for security)
- Python version and installed packages
- Azure DevOps connection status
- Email configuration status

### **Artifacts:**
Generated reports are saved as artifacts:
- HTML reports
- JSON data files
- Available for 7 days

## 📊 **Monitoring and Alerts**

### **Daily Reports:**
- **Time**: 5:00 PM IST (11:30 AM UTC)
- **Backup**: 6:00 PM IST (12:30 PM UTC)
- **Email**: Sent automatically to configured recipients
- **Status**: Available in GitHub Actions logs

### **Success Indicators:**
- ✅ All steps completed successfully
- 📧 Email received with report
- 📊 Reports generated and uploaded
- 🚀 Workflow status shows "Success"

## 🔄 **Maintenance and Updates**

### **Updating Secrets:**
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Find the secret to update
3. Click **Update** button
4. Enter new value
5. Click **Update secret**

### **Workflow Updates:**
- Edit `.github/workflows/daily-report.yml`
- Push changes to main branch
- Workflow automatically uses updated configuration

## 🎯 **Expected Results**

### **Daily at 5:00 PM IST:**
1. **Azure DevOps**: Extracts latest sprint data
2. **Report Generation**: Creates professional HTML report
3. **Email Delivery**: Sends report via Gmail SMTP
4. **GitHub Actions**: Logs all activities and results
5. **Artifacts**: Saves reports for 7 days

### **Manual Execution:**
- Run anytime via "Run workflow" button
- Same process as scheduled runs
- Immediate execution and results

## 🌟 **Benefits of GitHub Actions**

### **✅ Automation:**
- Runs automatically every day
- No manual intervention needed
- Consistent execution time

### **✅ Reliability:**
- GitHub's infrastructure
- Automatic retries on failure
- Detailed logging and monitoring

### **✅ Security:**
- Secrets encrypted and secure
- No credentials in code
- Repository-level access control

### **✅ Integration:**
- Seamless with your repository
- Version control integration
- Easy rollback and updates

## 🎉 **Success Checklist**

- [ ] All 6 secrets added to repository
- [ ] Workflow file exists in `.github/workflows/`
- [ ] Manual workflow trigger works
- [ ] No error messages in workflow logs
- [ ] Email received successfully
- [ ] Azure DevOps data extracted correctly
- [ ] Reports generated and uploaded
- [ ] Scheduled runs working at 5:00 PM IST

---

**Need help?** Check the workflow logs in the Actions tab for detailed error messages and debugging information.

**Your Azure DevOps AI Agent will now run automatically every day at 5:00 PM IST via GitHub Actions!** 🚀✨
