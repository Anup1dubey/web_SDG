# 🔧 MySQL Setup Instructions

## ✅ Configuration Complete!

Your backend is now ready to use MySQL. Follow these steps:

---

## Step 1: Configure MySQL Credentials

Edit `backend/.env` file and update with your MySQL details:

```env
# Database Configuration
DB_TYPE=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password_here
MYSQL_DATABASE=sdg_platform
```

**Important:** Replace `your_mysql_password_here` with your actual MySQL root password!

---

## Step 2: Create Database and Tables

Run the setup script:

```bash
cd backend
python setup_mysql.py
```

This will:
- ✅ Create the `sdg_platform` database
- ✅ Create all required tables (users, digital_twins, projects, organizations, etc.)

---

## Step 3: Stop Current Backend (if running)

```powershell
# Find and stop the backend process
Get-Process python | Where-Object {$_.MainWindowTitle -eq ""} | Stop-Process -Force
```

---

## Step 4: Start Backend with MySQL

```bash
cd backend
python run_server_simple.py
```

You should see:
```
✅ Database type: mysql
✅ Connected to: sdg_platform
```

---

## 🐛 Troubleshooting

### Error: "Access denied for user"
**Solution:** Check your MySQL password in `backend/.env`

### Error: "Can't connect to MySQL server"
**Solutions:**
1. Make sure MySQL service is running
2. Check if MySQL port (3306) is correct
3. Try `MYSQL_HOST=127.0.0.1` instead of `localhost`

### Error: "Unknown database"
**Solution:** Run `python setup_mysql.py` to create the database

### Want to switch back to SQLite?
Edit `backend/.env`:
```env
DB_TYPE=sqlite
```

---

## 🔍 Verify MySQL Connection

You can verify data is being saved to MySQL:

```sql
-- Connect to MySQL
mysql -u root -p

-- Use the database
USE sdg_platform;

-- Show tables
SHOW TABLES;

-- Check users table
SELECT * FROM users;

-- Check digital twins
SELECT * FROM digital_twins;
```

---

## 📊 Database Tables Created

The following tables will be created:
- `users` - User accounts
- `digital_twins` - Digital twin models
- `sdg_indicators` - SDG indicator values
- `organizations` - Organizations
- `projects` - SDG projects
- `simulations` - Simulation results
- `partnerships` - Partnership requests

---

## 🚀 Quick Commands

```bash
# Setup MySQL database
python backend/setup_mysql.py

# Start backend with MySQL
cd backend
python run_server_simple.py

# Start frontend
cd frontend
python -m http.server 3000
```

---

## 💡 Tips

1. **Development:** Use SQLite (easier, no setup)
2. **Production:** Use MySQL (better performance, scalability)
3. **Cloud:** Consider Railway, PlanetScale, or AWS RDS for hosted MySQL

---

## ✅ Ready!

Once you've configured MySQL credentials and run the setup script, your application will use MySQL instead of SQLite!
