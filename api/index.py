import sys
import os

from django.core.wsgi import get_wsgi_application

# Replace this with your actual project folder name
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "studentstudyportal.settings")

application = get_wsgi_application()
