"""
WSGI config for ithihas_project project.
"""

import os
import sys
from pathlib import Path

# Get the path to the root directory (where manage.py lives)
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ithihas_project.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()