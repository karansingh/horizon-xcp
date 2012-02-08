import logging
import os
import sys
import site

#KDS: added this to make wsgi play nice with virtual environment
# One directory above the project, so project name will be needed for imports
root_dir = '/usr/local/horizon/openstack-dashboard'

# with mod_wsgi >= 2.4, this line will add this path in front of the python path
site.addsitedir(os.path.join(root_dir, '.dashboard-venv/lib/python2.6/site-packages'))

# add this django project
sys.path.append(root_dir)

import django.core.handlers.wsgi
from django.conf import settings

# Add this file path to sys.path in order to import settings
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'
sys.stdout = sys.stderr

#KDS DEBUG = False
DEBUG = True

application = django.core.handlers.wsgi.WSGIHandler()

