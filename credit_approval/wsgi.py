"""
WSGI config for credit_approval project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_approval.settings')

# Auto-run migrations for Render Free Tier (Ephemeral Filesystem)
from django.core.management import call_command
try:
    call_command('migrate')
except Exception as e:
    print(f"Error running migrations: {e}")

application = get_wsgi_application()
