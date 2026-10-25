"""
api/index.py
Vercel Serverless Function Entrypoint.
Routes all requests to the Flask WSGI application instance.
"""

import sys
import os

# Add project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_app import app

# Vercel looks for the WSGI application callable 'app'
app = app
