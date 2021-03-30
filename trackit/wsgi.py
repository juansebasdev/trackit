"""
WSGI config for trackit project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/pi/trackit-omnia/')

os.environ['DJANGO_SETTINGS_MODULE']="trackit.settings"
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackit.settings')

os.environ.setdefault("LANG", "en_US.UTF-8")
os.environ.setdefault("LC_ALL", "en_US.UTF-8")

activate_this = '/home/pi/envs/gps/bin/activate_this.py'

exec(open(activate_this).read())

application = get_wsgi_application()
