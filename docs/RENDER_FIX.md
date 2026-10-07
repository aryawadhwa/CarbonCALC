# Render.com Build Fix

## Problem
Build error: `Cannot import 'setuptools.build_meta'`

This happens because:
1. Python 3.13 is too new (Render default)
2. setuptools not explicitly installed
3. Build dependencies missing

## Solution Applied

### 1. Added to requirements.txt
```
setuptools>=65.5.0
wheel>=0.38.0
```
(These are now at the top of requirements.txt)

### 2. Updated runtime.txt
Changed from `python-3.11.0` to `python-3.11.9` (more stable)

### 3. Updated render.yaml
Added pip upgrade in build command:
```yaml
buildCommand: pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python init_db.py
```

## Next Steps

1. **Commit and push these changes:**
   ```bash
   git add requirements.txt runtime.txt render.yaml
   git commit -m "Fix Render.com build: Add setuptools and update Python version"
   git push
   ```

2. **Redeploy on Render:**
   - Go to Render dashboard
   - Your service will auto-redeploy when you push
   - Or manually click "Manual Deploy" → "Deploy latest commit"

3. **Verify Build:**
   - Check build logs
   - Should now succeed! ✅

## Alternative: Manual Render Settings

If using Render dashboard (not render.yaml):

1. **Environment**: Python 3
2. **Python Version**: 3.11.9
3. **Build Command**: 
   ```
   pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python init_db.py
   ```
4. **Start Command**: 
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

## Why This Works

- **setuptools**: Required for building Python packages
- **wheel**: Modern package format, faster installs
- **Python 3.11.9**: More stable than 3.13, better package compatibility
- **pip upgrade**: Ensures latest pip has setuptools support

---

**After pushing, your Render deployment should build successfully!** 🚀

