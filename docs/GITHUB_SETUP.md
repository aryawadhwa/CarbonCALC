# GitHub Repository Setup Guide

Complete step-by-step guide to create a GitHub repository and push your CarbonCALC code.

---

## Method 1: Using GitHub Website + Command Line (Recommended)

### Step 1: Create Repository on GitHub Website

1. **Go to GitHub**
   - Visit https://github.com
   - Sign in (or create account if needed)

2. **Create New Repository**
   - Click the **"+" icon** (top right)
   - Select **"New repository"**

3. **Fill Repository Details**
   - **Repository name**: `CarbonCALC` (or `carboncalc` or `carbon-calc`)
   - **Description**: `Real-Time Carbon Footprint Monitoring and Predictive Reporting Cloud Solution`
   - **Visibility**: 
     - Choose **Public** (if you want it visible)
     - Choose **Private** (if you want it private)
   - ⚠️ **DO NOT** check:
     - ❌ "Add a README file" (we already have one)
     - ❌ "Add .gitignore" (we already have one)
     - ❌ "Choose a license" (you can add later)
   - Click **"Create repository"**

4. **Copy Repository URL**
   - GitHub will show you a page with commands
   - **Copy the repository URL** (looks like: `https://github.com/yourusername/CarbonCALC.git`)
   - Save it - you'll need it in the next step

---

### Step 2: Push Code from Your Computer

#### Open Terminal/Command Prompt

**On macOS/Linux:**
- Open **Terminal**

**On Windows:**
- Open **Command Prompt** or **PowerShell**
- Or use **Git Bash** (if installed)

#### Navigate to Your Project Folder

```bash
cd /Users/aryawadhwa/Desktop/CarbonCalc
```

(Or wherever your CarbonCalc folder is located)

---

### Step 3: Initialize Git (If Not Already Done)

```bash
# Initialize git repository (if not already done)
git init

# Check status
git status
```

---

### Step 4: Add All Files

```bash
# Add all files to git
git add .

# Verify files are staged
git status
```

You should see all your files listed as "Changes to be committed".

---

### Step 5: Make First Commit

```bash
# Create your first commit
git commit -m "Initial commit: CarbonCALC project setup"

# Or a more descriptive message:
git commit -m "Initial commit: CarbonCALC - Real-time carbon footprint monitoring with ML predictions and IoT integration"
```

---

### Step 6: Connect to GitHub Repository

```bash
# Add GitHub repository as remote (replace with YOUR repository URL)
git remote add origin https://github.com/yourusername/CarbonCALC.git

# Verify remote was added
git remote -v
```

**Important**: Replace `yourusername` with your actual GitHub username!

---

### Step 7: Push Code to GitHub

```bash
# Push to GitHub (first time)
git push -u origin main
```

If you get an error about branch names:
```bash
# If your branch is called 'master' instead of 'main'
git branch -M main
git push -u origin main
```

---

### Step 8: Authenticate

**If asked for credentials:**

- **Username**: Your GitHub username
- **Password**: Use a **Personal Access Token** (not your GitHub password)

**To create Personal Access Token:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "CarbonCALC"
4. Select scopes: Check **"repo"** (gives full repository access)
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)
7. Use this token as your password when pushing

---

### Step 9: Verify Upload

1. Go back to your GitHub repository page
2. Refresh the page
3. You should see all your files there! ✅

---

## Method 2: Using GitHub Desktop (Easier for Beginners)

### Step 1: Install GitHub Desktop

1. Download from: https://desktop.github.com
2. Install and sign in with your GitHub account

### Step 2: Add Repository

1. Open GitHub Desktop
2. Click **"File" → "Add Local Repository"**
3. Browse to your CarbonCalc folder: `/Users/aryawadhwa/Desktop/CarbonCalc`
4. Click "Add Repository"

### Step 3: Publish to GitHub

1. In GitHub Desktop, click **"Publish repository"** (top right)
2. Fill in:
   - **Name**: `CarbonCALC`
   - **Description**: `Real-Time Carbon Footprint Monitoring System`
   - Check/uncheck **"Keep this code private"** as desired
3. Click **"Publish Repository"**
4. Done! ✅

---

## Method 3: Using GitHub CLI (Advanced)

### Step 1: Install GitHub CLI

```bash
# macOS
brew install gh

# Or download from: https://cli.github.com
```

### Step 2: Authenticate

```bash
gh auth login
```

### Step 3: Create and Push

```bash
cd /Users/aryawadhwa/Desktop/CarbonCalc
git init
git add .
git commit -m "Initial commit: CarbonCALC"
gh repo create CarbonCALC --public --source=. --remote=origin --push
```

---

## Common Issues and Solutions

### Issue 1: "Repository not found"

**Solution**: Check your repository URL is correct
```bash
git remote -v  # Check remote URL
git remote set-url origin https://github.com/yourusername/CarbonCALC.git  # Fix it
```

### Issue 2: "Authentication failed"

**Solution**: Use Personal Access Token instead of password
- Create token: GitHub → Settings → Developer settings → Personal access tokens
- Use token as password when prompted

### Issue 3: "Branch 'main' does not exist"

**Solution**: 
```bash
git branch -M main  # Rename current branch to main
git push -u origin main
```

### Issue 4: "Large files" or upload too slow

**Solution**: Check `.gitignore` is working
```bash
git status  # See what's being uploaded
# Large files should be in .gitignore
```

### Issue 5: "Permission denied"

**Solution**: 
- Make sure you're authenticated
- Check repository name matches
- Verify you have write access to the repo

---

## After Pushing: Next Steps

### 1. Add Repository Description
- Go to your GitHub repo
- Click "Settings" → Edit repository description
- Add: "Real-Time Carbon Footprint Monitoring and Predictive Reporting Cloud Solution"

### 2. Add Topics/Tags
- On repo page, click the gear icon next to "About"
- Add topics: `carbon-footprint`, `machine-learning`, `iot`, `sustainability`, `fastapi`, `python`

### 3. Update README (Optional)
- Your README.md is already great!
- You can add badges, screenshots, etc.

### 4. Set Up GitHub Pages (Optional - for frontend only)
- If you want to host just the frontend on GitHub Pages
- See DEPLOYMENT.md for full backend deployment

---

## Quick Reference Commands

```bash
# Navigate to project
cd /Users/aryawadhwa/Desktop/CarbonCalc

# Initialize git (first time only)
git init

# Add all files
git add .

# Commit changes
git commit -m "Your commit message"

# Connect to GitHub (first time only)
git remote add origin https://github.com/yourusername/CarbonCALC.git

# Push to GitHub
git push -u origin main

# Check status
git status

# View remote
git remote -v
```

---

## Future Updates

After initial push, to update your repository:

```bash
# Navigate to project folder
cd /Users/aryawadhwa/Desktop/CarbonCalc

# Add changes
git add .

# Commit changes
git commit -m "Description of what you changed"

# Push to GitHub
git push
```

---

## Summary Checklist

- [ ] Created GitHub account
- [ ] Created new repository on GitHub
- [ ] Opened terminal/command prompt
- [ ] Navigated to CarbonCalc folder
- [ ] Ran `git init`
- [ ] Ran `git add .`
- [ ] Ran `git commit -m "Initial commit"`
- [ ] Added remote: `git remote add origin <your-repo-url>`
- [ ] Pushed: `git push -u origin main`
- [ ] Verified files on GitHub
- [ ] Created Personal Access Token (if needed)

---

## Need Help?

- GitHub Docs: https://docs.github.com
- Git Basics: https://git-scm.com/book/en/v2/Getting-Started-Git-Basics
- GitHub Desktop: https://docs.github.com/en/desktop

---

**You're all set! Your CarbonCALC code is now on GitHub! 🚀**

