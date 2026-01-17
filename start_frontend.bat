@echo off
echo ============================================================
echo    SDG DIGITAL TWIN PLATFORM - FRONTEND SERVER
echo ============================================================
echo.
echo 🌐 Starting Frontend Server...
echo 🔗 Application URL: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

cd frontend
echo Starting HTTP server on port 3000...
python -m http.server 3000
