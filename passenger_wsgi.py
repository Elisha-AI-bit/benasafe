import os
import sys

# Add the project directory to the sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Import the application from the project's wsgi.py
# Make sure 'bene_safe' matches your project folder name
from bene_safe.wsgi import application
