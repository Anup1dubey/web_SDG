#!/usr/bin/env python3
"""
SDG Digital Twin Platform - Server Runner
Starts the FastAPI backend server
"""
import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("🌍 SDG DIGITAL TWIN & FUTURE IMPACT SIMULATION PLATFORM")
    print("=" * 60)
    print("\n🚀 Starting Backend API Server...")
    print("📡 API Documentation: http://localhost:8000/docs")
    print("🔗 API Base URL: http://localhost:8000")
    print("\n💡 Make sure to run the frontend on a separate server!")
    print("   Example: python -m http.server 3000 (in frontend folder)")
    print("\n" + "=" * 60 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
