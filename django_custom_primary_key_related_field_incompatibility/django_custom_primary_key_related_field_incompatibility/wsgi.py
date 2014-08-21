"""
WSGI config for django_custom_primary_key_related_field_incompatibility project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_custom_primary_key_related_field_incompatibility.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
