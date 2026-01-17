# 📦 Installation Guide

## **Complete Setup Instructions**

---

## **Prerequisites**

### **Required Software:**
- **Python 3.8 or higher** - [Download here](https://www.python.org/downloads/)
  - ✅ Make sure to check "Add Python to PATH" during installation
- **Web Browser** - Chrome, Firefox, Edge, or Safari
- **Terminal/Command Prompt** access

### **Optional (for development):**
- Git for version control
- VS Code or any code editor
- Postman for API testing

---

## **Installation Steps**

### **Method 1: Automated Setup (Windows - Recommended)**

#### **Step 1: Run Setup Script**

1. Double-click `setup.bat`
2. Wait for installation to complete (2-3 minutes)
3. You should see: `✅ SETUP COMPLETE!`

#### **Step 2: Start Backend Server**

1. Double-click `start_backend.bat`
2. Wait for message: `Application startup complete`
3. Keep this window open

#### **Step 3: Start Frontend Server**

1. Open a **new** terminal/command prompt
2. Double-click `start_frontend.bat`
3. You should see: `Serving HTTP on 0.0.0.0 port 3000`

#### **Step 4: Open Application**

1. Open your browser
2. Navigate to: `http://localhost:3000`
3. You should see the SDG Digital Twin Platform

✅ **Done! Start using the platform.**

---

### **Method 2: Manual Setup (All Platforms)**

#### **Step 1: Verify Python Installation**

```bash
python --version
# Should show Python 3.8 or higher

# If "python" doesn't work, try:
python3 --version
```

#### **Step 2: Install Backend Dependencies**

```bash
# Navigate to backend folder
cd backend

# Install required packages
pip install -r requirements.txt

# If pip doesn't work, try:
pip3 install -r requirements.txt

# Or use python -m pip:
python -m pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastapi-0.109.0 uvicorn-0.27.0 sqlalchemy-2.0.25 ...
```

#### **Step 3: Initialize Database**

```bash
# Still in backend folder
python -c "from database import init_db; init_db(); print('Database initialized')"
```

**Expected output:**
```
Database initialized
```

#### **Step 4: (Optional) Seed Demo Data**

```bash
python seed_demo_data.py
```

**Expected output:**
```
🌱 SEEDING DEMO DATA
✅ Created 5 organizations
✅ Created Mumbai Digital Twin (ID: 1)
✅ Created Copenhagen Digital Twin (ID: 2)
✅ Created Kenya Digital Twin (ID: 3)
✅ Created 8 projects
✅ DEMO DATA SEEDING COMPLETE!
```

#### **Step 5: Start Backend Server**

```bash
python run_server.py
```

**Expected output:**
```
🌍 SDG DIGITAL TWIN & FUTURE IMPACT SIMULATION PLATFORM
🚀 Starting Backend API Server...
📡 API Documentation: http://localhost:8000/docs
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**✅ Backend is running!** Leave this terminal open.

#### **Step 6: Start Frontend Server**

Open a **NEW** terminal window:

```bash
# Navigate to frontend folder
cd frontend

# Start HTTP server
python -m http.server 3000

# If python doesn't work, try:
python3 -m http.server 3000
```

**Expected output:**
```
Serving HTTP on 0.0.0.0 port 3000 (http://0.0.0.0:3000/) ...
```

**✅ Frontend is running!** Leave this terminal open.

#### **Step 7: Open Application**

1. Open browser to: `http://localhost:3000`
2. You should see the platform interface

---

## **Verification Checklist**

After installation, verify everything works:

- [ ] Backend API responds at `http://localhost:8000`
- [ ] API docs load at `http://localhost:8000/docs`
- [ ] Frontend loads at `http://localhost:3000`
- [ ] Can create a Digital Twin
- [ ] Can run a simulation
- [ ] Charts render correctly
- [ ] No console errors in browser (F12)

---

## **Troubleshooting**

### **Problem: "pip not found" or "python not found"**

**Solution:**
1. Verify Python is installed: Search for "Python" in your programs
2. Reinstall Python with "Add to PATH" option checked
3. Try `python3` and `pip3` instead of `python` and `pip`
4. Restart your terminal after installation

### **Problem: "ModuleNotFoundError: No module named 'fastapi'"**

**Solution:**
```bash
cd backend
pip install -r requirements.txt --upgrade
```

### **Problem: Backend starts but shows errors**

**Solution:**
```bash
# Reset the database
cd backend
python -c "from database import Base, engine; Base.metadata.drop_all(engine); Base.metadata.create_all(engine); print('Database reset')"
```

### **Problem: "Port 8000 already in use"**

**Solution:**

**Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

**Mac/Linux:**
```bash
lsof -ti:8000 | xargs kill -9
```

Or change the port in `backend/run_server.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed to 8001
```

### **Problem: "Port 3000 already in use"**

**Solution:**
```bash
# Use a different port
python -m http.server 8080

# Then open: http://localhost:8080
```

### **Problem: Frontend loads but shows "Connection refused"**

**Solution:**
1. Verify backend is running: Open `http://localhost:8000` in browser
2. Check for CORS errors in browser console (F12)
3. Restart backend server
4. Check firewall settings

### **Problem: Database errors**

**Solution:**
```bash
cd backend
# Delete old database
rm sdg_platform.db  # Linux/Mac
del sdg_platform.db  # Windows

# Recreate
python -c "from database import init_db; init_db()"
```

### **Problem: Charts not rendering**

**Solution:**
1. Check browser console (F12) for JavaScript errors
2. Verify Chart.js is loading (check Network tab)
3. Try a different browser
4. Clear browser cache (Ctrl+Shift+Delete)

---

## **Alternative: Using Virtual Environment (Recommended for Development)**

### **Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run_server.py
```

### **Mac/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run_server.py
```

To deactivate:
```bash
deactivate
```

---

## **Testing the Installation**

### **Test 1: API Health Check**

Open browser to: `http://localhost:8000`

**Expected response:**
```json
{
  "message": "SDG Digital Twin & Future Impact Simulation Platform",
  "version": "1.0.0",
  "innovation": "Predict future SDG outcomes before they happen"
}
```

### **Test 2: Get SDGs**

Open: `http://localhost:8000/sdgs`

**Expected:** JSON with all 17 SDG definitions

### **Test 3: API Documentation**

Open: `http://localhost:8000/docs`

**Expected:** Interactive Swagger UI with all endpoints

### **Test 4: Frontend Load**

Open: `http://localhost:3000`

**Expected:** SDG Digital Twin Platform homepage with navigation

### **Test 5: Create Digital Twin**

1. Click "Digital Twins" tab
2. Click "+ Create Digital Twin"
3. Fill form:
   - Name: Test Twin
   - Region: Test City
   - Country: Test Country
   - Population: 1000000
   - Area: 100
4. Submit

**Expected:** New twin appears in grid

### **Test 6: Run Simulation**

1. Click "Future Simulation" tab
2. Select your test twin
3. Click SDG 6 and SDG 11
4. Click "🚀 Run Simulation"

**Expected:** Results appear with charts and explanations

---

## **Post-Installation**

### **Recommended Next Steps:**

1. **Seed demo data** for better demonstrations:
   ```bash
   cd backend
   python seed_demo_data.py
   ```

2. **Read the documentation:**
   - `README.md` - Full documentation
   - `DEMO_SCRIPT.md` - Presentation guide
   - `QUICKSTART.md` - Quick usage guide

3. **Explore the API:**
   - Visit `http://localhost:8000/docs`
   - Try different endpoints
   - Test simulation with different parameters

4. **Customize the platform:**
   - Edit simulation coefficients in `backend/simulation_engine.py`
   - Modify UI styles in `frontend/styles.css`
   - Add new SDG indicators in `backend/sdg_data.py`

---

## **Uninstallation**

To remove the platform:

1. Stop both servers (Ctrl+C in terminals)
2. Delete the project folder
3. (Optional) Uninstall Python packages:
   ```bash
   pip uninstall fastapi uvicorn sqlalchemy pymysql pydantic numpy scikit-learn
   ```

---

## **Getting Help**

### **Check Logs:**

**Backend logs:** Look at the terminal running the backend server

**Frontend logs:** Open browser console (F12 → Console tab)

**Database issues:** Check if `backend/sdg_platform.db` file exists

### **Common Error Messages:**

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `Port already in use` | Kill the process or use a different port |
| `Database is locked` | Close all connections and restart |
| `CORS error` | Restart backend server |
| `404 Not Found` | Check URL spelling and server status |

---

## **System Requirements**

### **Minimum:**
- CPU: Dual-core processor
- RAM: 2 GB
- Disk: 500 MB free space
- OS: Windows 10, macOS 10.14, Ubuntu 18.04 or newer

### **Recommended:**
- CPU: Quad-core processor
- RAM: 4 GB
- Disk: 1 GB free space
- SSD for better database performance

---

## **Browser Compatibility**

✅ **Fully Supported:**
- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

⚠️ **Limited Support:**
- Internet Explorer (not recommended)
- Older mobile browsers

---

## **Network Configuration**

### **Default Ports:**
- Backend: `8000`
- Frontend: `3000`

### **Firewall Settings:**

If blocked, allow incoming connections on:
- Port 8000 (Backend)
- Port 3000 (Frontend)

**Windows Firewall:**
1. Settings → Update & Security → Windows Security
2. Firewall & network protection → Allow an app
3. Add Python and allow on private networks

---

## **Production Deployment (Future)**

For production deployment, consider:

1. **Use a production WSGI server** (Gunicorn)
2. **Set up reverse proxy** (NGINX)
3. **Use PostgreSQL** instead of SQLite
4. **Enable HTTPS** with SSL certificates
5. **Add authentication** (JWT tokens)
6. **Set up monitoring** (Prometheus, Grafana)
7. **Configure backups** for database
8. **Use environment variables** for sensitive data

See `ARCHITECTURE.md` for deployment architecture.

---

## **Success!** 🎉

If you've completed all steps, you now have a fully functional SDG Digital Twin & Future Impact Simulation Platform running locally!

**Next:** Check out `QUICKSTART.md` for your first simulation or `DEMO_SCRIPT.md` for presentation tips.

**Questions?** Review the troubleshooting section or check the main `README.md`.

---

**Ready to predict the future? Let's go!** 🚀🌍
