"""
WSGI config for TAPP project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TAPP.settings")

from django.core.wsgi import get_wsgi_application
from settings import DEPLOY_MODE
if DEPLOY_MODE == 'development':
    application = get_wsgi_application()
elif DEPLOY_MODE == 'production':
    from dj_static import Cling
    application = Cling(get_wsgi_application())
