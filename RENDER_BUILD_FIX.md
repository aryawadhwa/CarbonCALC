# Render.com Build Fix - Step by Step

## Current Issue
Build error: `Cannot import 'setuptools.build_meta'`

This happens because Render is using Python 3.13 (too new) or setuptools isn't installing correctly.

---

## Solution: Manual Render Configuration

Since Render might not be reading `render.yaml` correctly, configure it manually:

### Step 1: Commit and Push Changes

```bash
git add requirements.txt runtime.txt render.yaml
git commit -m "Fix Render build: Add setuptools, update Python to 3.11"
git push
```

### Step 2: Update Render Settings Manually

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Click on your service (carboncalc)

2. **Go to Settings Tab**

3. **Update Build & Deploy Settings:**

   **Build Command:**
   ```
   pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python init_db.py
   ```

   **Start Command:**
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **Set Python Version:**
   - Scroll to "Environment" section
   - Click "Add Environment Variable"
   - Key: `PYTHON_VERSION`
   - Value: `3.11.9`
   - Save

5. **Manual Deploy:**
   - Click "Manual Deploy" dropdown
   - Select "Clear build cache & deploy"
   - This forces a fresh build

---

## Alternative: Use requirements.txt Only

If the above doesn't work, ensure requirements.txt has everything at the top:

```txt
setuptools>=65.5.0
wheel>=0.38.0
pip>=23.0.0
fastapi==0.104.1
...
```

---

## Verify Your Files

Check these files are correct:

### runtime.txt should have:
```
python-3.11.9
```

### requirements.txt should START with:
```
setuptools>=65.5.0
wheel>=0.38.0
...
```

### Build command should be:
```
pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python init_db.py
```

---

## If Still Failing

### Option 1: Try Python 3.10 (More Stable)
In Render dashboard, set:
- Environment Variable: `PYTHON_VERSION` = `3.10.12`

Update runtime.txt:
```
python-3.10.12
```

### Option 2: Use Pipfile (Alternative)
Some users have success with Pipfile instead of requirements.txt.

### Option 3: Contact Render Support
If nothing works, Render support is very helpful!

---

## Quick Checklist

- [ ] `setuptools>=65.5.0` is FIRST in requirements.txt
- [ ] `runtime.txt` specifies Python 3.11.9 (or 3.10.12)
- [ ] Build command includes `pip install --upgrade pip setuptools wheel`
- [ ] Changes committed and pushed to GitHub
- [ ] Render dashboard: PYTHON_VERSION environment variable set
- [ ] Manual deploy with cleared cache

---

**After making these changes, your build should succeed!** ✅

