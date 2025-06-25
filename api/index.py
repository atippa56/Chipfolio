import sys
import os

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

# Import and export the FastAPI app
from app.main import app

# Vercel handler
app = app

# Vercel expects a handler function
def handler(request, response):
    return app

# Also export the app directly for Vercel
__all__ = ['app', 'handler'] 