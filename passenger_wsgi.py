import os
import sys

# path to your app
sys.path.insert(0, os.path.dirname(__file__))

# change PROJECTNAME to your Django project folder
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bene_safe.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
