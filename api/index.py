"""
Vercel Serverless Function Entry Point
This file adapts the FastAPI app for Vercel's serverless environment
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from main import app

# Vercel serverless function handler
handler = app
