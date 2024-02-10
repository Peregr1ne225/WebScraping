import os
import django
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebScapping.settings")
django.setup()