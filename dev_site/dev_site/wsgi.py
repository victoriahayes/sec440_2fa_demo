"""
WSGI config for dev_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os, logging, sys

from django.core.wsgi import get_wsgi_application

dir_path = os.path.dirname(os.path.realpath(__file__))
par_dir = os.path.abspath(os.path.join(dir_path, os.pardir))

sys.path.append(par_dir)
logging.basicConfig(stream=sys.stderr)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dev_site.settings")

application = get_wsgi_application()
