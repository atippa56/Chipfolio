import sys
import os

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

# Import the FastAPI app
from app.main import app

# Export the app directly - Vercel will handle this automatically
# The app variable will be used by Vercel's Python runtime 