# 🚨 Troubleshooting Guide for GitHub Actions

## 🔍 **Common Issues and Solutions**

### **Issue 1: "Missing required environment variables"**

#### **Symptoms:**
```
⚠️ Missing required environment variables: EMAIL_FROM, EMAIL_TO, SMTP_USERNAME, SMTP_PASSWORD
❌ Configuration validation failed
```

#### **Root Cause:**
The workflow is running but the repository secrets are not properly configured or accessible.

#### **Solutions:**

##### **A. Check Repository Secrets**
1. Go to your repository: `https://github.com/gourav8jain/ai-agent-azure-devops-reporting`
2. Click **Settings** tab
3. Click **Secrets and variables** → **Actions**
4. Verify these 6 secrets exist:

| Secret Name | Required Value |
|-------------|----------------|
| `AZURE_DEVOPS_ORG` | `delhivery` |
| `AZURE_DEVOPS_PAT` | `YOUR_AZURE_DEVOPS_PAT_HERE` |
| `EMAIL_FROM` | `gourav8jain@gmail.com` |
| `EMAIL_TO` | `gourav8jain@gmail.com` |
| `SMTP_USERNAME` | `gourav8jain@gmail.com` |
| `SMTP_PASSWORD` | `YOUR_GMAIL_APP_PASSWORD_HERE` |

##### **B. Verify Secret Names**
- **Case-sensitive**: Secret names must match exactly
- **No spaces**: Ensure no leading/trailing spaces
- **Correct format**: Use exact names from the table above

##### **C. Check Repository Permissions**
1. Go to **Settings** → **Actions** → **General**
2. Ensure **Actions permissions** is set to **Allow all actions and reusable workflows**
3. Check if there are any workflow restrictions

#### **Issue 2: "Workflow not running automatically"**

#### **Symptoms:**
- Workflow doesn't run at scheduled time (10:30 AM IST)
- No automatic execution

#### **Solutions:**

##### **A. Check Workflow File**
- Verify `.github/workflows/daily-report.yml` exists
- Ensure file is committed to main branch
- Check for syntax errors in YAML

##### **B. Test Manual Execution**
1. Go to **Actions** tab
2. Click **Daily Sprint Report**
3. Click **Run workflow**
4. Select **main** branch
5. Click **Run workflow**

##### **C. Check Repository Activity**
- GitHub may pause workflows for inactive repositories
- Make a small commit to trigger workflow
- Check if workflow runs on push

#### **Issue 3: "Authentication failed"**

#### **Symptoms:**
- Azure DevOps connection fails
- Gmail SMTP authentication fails

#### **Solutions:**

##### **A. Azure DevOps PAT**
- Check if PAT is expired
- Verify PAT has correct permissions
- Ensure PAT is valid for the organization

##### **B. Gmail Authentication**
- Verify 2-factor authentication is enabled
- Check App Password is correct
- Ensure account is not locked

#### **Issue 4: "Python dependencies failed"**

#### **Symptoms:**
- Workflow fails during dependency installation
- Import errors in scripts

#### **Solutions:**

##### **A. Check requirements.txt**
- Verify all required packages are listed
- Check for syntax errors
- Ensure package versions are compatible

##### **B. Python Version**
- Workflow uses Python 3.9
- Ensure code is compatible with this version

## 🔧 **Debugging Steps**

### **Step 1: Check Workflow Logs**
1. Go to **Actions** tab
2. Click on failed workflow run
3. Click on failed step
4. Review error messages and logs

### **Step 2: Test Configuration Locally**
```bash
# Test configuration validation
python3 test_github_actions.py

# Test complete workflow
python3 run_complete_workflow.py
```

### **Step 3: Verify Environment Variables**
```bash
# Check if .env file exists and has correct values
cat .env

# Test configuration import
python3 -c "from config import Config; Config.validate_config()"
```

### **Step 4: Check GitHub Actions Environment**
The workflow now includes comprehensive debugging:
- Environment variable status
- Python version and packages
- Configuration validation results
- Step-by-step execution logs

## 🚀 **Prevention and Best Practices**

### **1. Repository Secrets Management**
- Use descriptive secret names
- Regularly rotate sensitive credentials
- Test secrets after updates
- Keep backup of credential values

### **2. Workflow Testing**
- Test manually before relying on schedule
- Monitor first few automatic runs
- Check logs for any warnings
- Verify email delivery

### **3. Code Quality**
- Validate configuration before execution
- Include comprehensive error handling
- Provide clear error messages
- Test locally before pushing

## 📋 **Quick Fix Checklist**

- [ ] All 6 repository secrets are set
- [ ] Secret names match exactly (case-sensitive)
- [ ] Workflow file exists in `.github/workflows/`
- [ ] Actions permissions are enabled
- [ ] Repository has recent activity
- [ ] Local testing passes
- [ ] Manual workflow trigger works

## 🆘 **Getting Help**

### **1. Check Workflow Logs First**
- Most issues are visible in the logs
- Look for specific error messages
- Check environment variable status

### **2. Test Locally**
- Run `python3 test_github_actions.py`
- Verify configuration works locally
- Check if .env file is correct

### **3. Common Solutions**
- **Missing secrets**: Add repository secrets
- **Permission issues**: Check Actions settings
- **Authentication failures**: Verify credentials
- **Dependency issues**: Check requirements.txt

## 🎯 **Expected Behavior**

### **Successful Workflow:**
1. ✅ All steps complete successfully
2. 📧 Email received with report
3. 📊 Reports generated and uploaded
4. 🚀 Workflow status shows "Success"
5. 📅 Next run scheduled automatically

### **Failed Workflow:**
1. ❌ Step fails with specific error
2. 📝 Detailed error message in logs
3. 🔍 Environment variable status shown
4. 💡 Suggested solutions provided
5. 🔄 Can be retried manually

---

**Remember**: Most issues are related to repository secrets or permissions. Check the workflow logs first, then verify your secrets configuration.

**Your Azure DevOps AI Agent should work reliably in GitHub Actions once all secrets are properly configured!** 🚀✨
