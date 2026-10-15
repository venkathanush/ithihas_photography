"""
WSGI config for ithihas_photography project.
"""

import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add the project directory and parent directory to Python path
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / 'ithihas_photography'))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ithihas_project.settings')

application = get_wsgi_application()