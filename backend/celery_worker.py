import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from tasks import celery, init_celery

app = create_app()

# Bind Celery to the Flask application
init_celery(app)