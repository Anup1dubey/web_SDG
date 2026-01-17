@echo off
echo ============================================================
echo    SDG DIGITAL TWIN PLATFORM - SETUP SCRIPT
echo ============================================================
echo.

echo [1/3] Installing Python dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [2/3] Initializing database...
python -c "from database import init_db; init_db(); print('✅ Database initialized')"
if %errorlevel% neq 0 (
    echo ERROR: Failed to initialize database
    pause
    exit /b 1
)
echo.

echo [3/3] Verifying installation...
python -c "from simulation_engine import SimulationEngine; print('✅ Simulation engine ready')"
if %errorlevel% neq 0 (
    echo ERROR: Simulation engine verification failed
    pause
    exit /b 1
)

cd ..
echo.
echo ============================================================
echo    ✅ SETUP COMPLETE!
echo ============================================================
echo.
echo Next steps:
echo   1. Run: start_backend.bat
echo   2. Run: start_frontend.bat (in a new terminal)
echo   3. Open: http://localhost:3000
echo.
pause
