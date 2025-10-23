# Troubleshooting: Render.com Deployment Issues

## Problem Summary

**Symptom:** HTML files `order-lists.html` and `meal-plans.html` return 404 on Render.com, despite being present in the Git repository and working locally.

**Status:** 
- ✅ Files exist in Git repository
- ✅ Files work locally (Flask dev server)
- ✅ Routes are defined in app.py
- ✅ Multiple deployments triggered
- ❌ Files return 404 on Render.com
- ❌ Health Check API returns 404 on Render.com

## Timeline of Actions Taken

### 1. Initial Implementation (Commit 43aa6ee)
- Created `order-lists.html` and `meal-plans.html`
- Added routes in `app.py`
- Pushed to GitHub

### 2. Route Fixes (Multiple commits)
- Added explicit routes for both HTML files
- Added debug logging
- Added catch-all route for static files

### 3. Deployment Attempts
- Multiple force deployments with empty commits
- File timestamp updates
- Git remove and re-add
- Deployment version tracking

### 4. Monitoring Implementation (Commit 0c4e8eb)
- Added health check API
- Added link monitoring script
- Comprehensive logging

### 5. Current Status
- Test file `test-render-deploy.html` created to verify deployment process
- Waiting for deployment to complete

## Verified Facts

### ✅ What Works Locally

```bash
# Local Flask server
python3 -c "
from backend.app import app
app.run(port=5556)
"

# Test URLs
curl http://localhost:5556/order-lists.html  # 200 OK
curl http://localhost:5556/meal-plans.html   # 200 OK
curl http://localhost:5556/api/health        # 200 OK
```

### ✅ What Works on Render.com

```bash
curl https://menuplan-simulator-v5.onrender.com/                  # 200 OK (landing.html)
curl https://menuplan-simulator-v5.onrender.com/index.html        # 200 OK
curl https://menuplan-simulator-v5.onrender.com/recipes.html      # 200 OK
curl https://menuplan-simulator-v5.onrender.com/analytics.html    # 200 OK
curl https://menuplan-simulator-v5.onrender.com/procurement.html  # 200 OK
curl https://menuplan-simulator-v5.onrender.com/api/recipes       # 200 OK
```

### ❌ What Doesn't Work on Render.com

```bash
curl https://menuplan-simulator-v5.onrender.com/order-lists.html      # 404
curl https://menuplan-simulator-v5.onrender.com/meal-plans.html       # 404
curl https://menuplan-simulator-v5.onrender.com/api/health            # 404
curl https://menuplan-simulator-v5.onrender.com/deployment-version    # 404
```

## Possible Root Causes

### 1. **Render.com Caching Issue**
- Render.com may be caching the old version of app.py
- Static files may be cached separately
- **Solution:** Clear Render.com build cache (manual action required in dashboard)

### 2. **Build Process Not Copying Files**
- Files may not be included in the build artifact
- **Solution:** Check Render.com build logs for file copying

### 3. **Gunicorn Static File Handling**
- Gunicorn may not serve static files the same way as Flask dev server
- **Solution:** Add explicit static file middleware or use WhiteNoise

### 4. **Import Error on Render.com**
- `health_check.py` import may be failing silently
- **Solution:** Check Render.com logs for import errors

### 5. **File Permissions**
- Files may have wrong permissions on Render.com
- **Solution:** Check file permissions in build logs

### 6. **Path Resolution Issue**
- `static_folder='../frontend'` may resolve differently on Render.com
- **Solution:** Use absolute paths

## Recommended Solutions

### Solution 1: Use WhiteNoise for Static Files

WhiteNoise is a Python library specifically designed to serve static files in production with Gunicorn.

**Install:**
```bash
pip install whitenoise
```

**Update app.py:**
```python
from whitenoise import WhiteNoise

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.wsgi_app = WhiteNoise(app.wsgi_app, root='frontend/', prefix='')
CORS(app)
```

**Update requirements.txt:**
```
whitenoise==6.6.0
```

### Solution 2: Absolute Path for static_folder

**Update app.py:**
```python
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, '..', 'frontend')

app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path='')
```

### Solution 3: Manual Render.com Actions

1. **Clear Build Cache:**
   - Go to Render.com Dashboard
   - Select the service
   - Click "Manual Deploy" → "Clear build cache & deploy"

2. **Check Build Logs:**
   - Look for file copying messages
   - Check for import errors
   - Verify Python version

3. **Check Runtime Logs:**
   - Look for "DEBUG:" messages
   - Check for route registration messages
   - Verify static_folder path

### Solution 4: Simplify Routes

Remove catch-all route and use only explicit routes:

```python
@app.route('/order-lists.html')
def order_lists():
    return send_from_directory(app.static_folder, 'order-lists.html')

@app.route('/meal-plans.html')
def meal_plans():
    return send_from_directory(app.static_folder, 'meal-plans.html')
```

### Solution 5: Use Nginx or Apache

If Flask/Gunicorn continues to have issues, consider using a proper web server:

**Update render.yaml:**
```yaml
services:
  - type: web
    name: menuplan-simulator
    env: docker
    dockerfilePath: ./Dockerfile
```

**Create Dockerfile:**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN pip install gunicorn
EXPOSE 5000
CMD ["gunicorn", "-c", "gunicorn.conf.py", "backend.app:app"]
```

## Diagnostic Commands

### Check File Existence on Render.com

Once `/api/health/files` is working:
```bash
curl https://menuplan-simulator-v5.onrender.com/api/health/files | jq '.files[] | select(.path | contains("order-lists") or contains("meal-plans"))'
```

### Check Detailed Health

```bash
curl https://menuplan-simulator-v5.onrender.com/api/health/detailed | jq '.checks'
```

### Monitor Deployment

```bash
python3 monitoring/link_monitor.py https://menuplan-simulator-v5.onrender.com
```

## Next Steps

1. **Wait for test file deployment** (test-render-deploy.html)
2. **If test file works:** Issue is specific to order-lists.html and meal-plans.html
3. **If test file doesn't work:** Issue is with all new files
4. **Implement WhiteNoise** as the most robust solution
5. **Manual Render.com intervention** if software solutions don't work

## Contact Render.com Support

If all solutions fail, contact Render.com support with:
- Service name: menuplan-simulator-v5
- Issue: New HTML files not being served despite being in repository
- Evidence: Working locally, 404 on production
- Logs: Build logs and runtime logs
- Repository: https://github.com/jb-x-dev/menuplan-simulator-v5

## Workaround

While debugging, users can access functionality through:
1. **Bestelllisten:** Use the "📋 Bestellvorschlag generieren" button in the main app
2. **Menüpläne:** Use the "💾 Menüplan speichern" button in the main app

The functionality exists, just the dedicated management pages are not accessible.

