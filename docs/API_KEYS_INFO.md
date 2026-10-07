# API Keys & External Services - Not Needed! ✅

## Good News: No External APIs Required!

Your CarbonCALC project **does NOT use any external APIs** that require API keys. Everything runs locally!

---

## What Your Project Uses (No Keys Needed)

### ✅ FastAPI Framework
- **What it is**: Python web framework (like Flask, but faster)
- **API Key needed?**: ❌ No
- **What it does**: Creates your REST API endpoints

### ✅ Local Calculations
- **What it is**: Carbon footprint calculator using emission factors
- **API Key needed?**: ❌ No
- **Source**: IPCC/EPA standard emission factors (hardcoded in your code)
- **Location**: `utils/carbon_calculator.py`

### ✅ Scikit-learn (ML Models)
- **What it is**: Python machine learning library
- **API Key needed?**: ❌ No
- **What it does**: Runs ML models on your server (CPU-based)

### ✅ SQLite/PostgreSQL Database
- **What it is**: Database for storing user data
- **API Key needed?**: ❌ No
- **Local**: SQLite (file-based)
- **Cloud**: PostgreSQL on Render.com (free, included)

---

## Optional: SECRET_KEY (For Security)

### What is SECRET_KEY?
- Used to sign JWT (JSON Web Tokens) for user authentication
- Keeps user sessions secure
- **You generate this yourself** - not an external API key!

### How to Generate SECRET_KEY:

#### Option 1: Python (Easiest)
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Option 2: Online Generator
- Visit: https://generate-secret.vercel.app/32
- Copy the generated string

#### Option 3: OpenSSL
```bash
openssl rand -hex 32
```

### Where to Set It:

**For Local Development:**
Create a `.env` file in your project root:
```env
SECRET_KEY=your-generated-secret-key-here
DATABASE_URL=sqlite:///./carbon_monitor.db
```

**For Production (Render.com):**
1. Go to Render dashboard
2. Select your service
3. Go to "Environment" tab
4. Add variable:
   - **Key**: `SECRET_KEY`
   - **Value**: (paste your generated key)
5. Save

### Current Default:
Your code has a default fallback:
```python
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
```

⚠️ **Important**: Change this default before deploying to production!

---

## Summary

| Component | External API? | API Key Needed? |
|-----------|--------------|-----------------|
| FastAPI | ❌ No | ❌ No |
| Carbon Calculator | ❌ No (local) | ❌ No |
| ML Models | ❌ No (local) | ❌ No |
| Database | ❌ No (self-hosted) | ❌ No |
| SECRET_KEY | ❌ No | ❌ No (you generate it) |

---

## What You DON'T Need

❌ Google Maps API key  
❌ Weather API key  
❌ OpenAI API key  
❌ Any third-party service API keys  
❌ Carbon footprint API subscription  

Everything is **self-contained** and runs on your server! 🎉

---

## Ready to Deploy

Since you don't need any external API keys, you can deploy immediately:

1. ✅ Push to GitHub (already done!)
2. ✅ Deploy to Render.com
3. ✅ Set SECRET_KEY in Render dashboard (optional but recommended)
4. ✅ Done!

See `DEPLOYMENT.md` for deployment instructions.

---

**Bottom Line**: Your project is completely self-contained. No API keys to find or configure! 🚀

