# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2011 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

#from django.conf.urls.defaults import *

#import horizon

#from horizon.dashboards.nova.images_and_snapshots.images import urls\
#                                                         as image_urls
#from horizon.dashboards.nova.images_and_snapshots.snapshots import urls\
#                                                            as snapshot_urls

#urlpatterns = patterns('horizon.dashboards.nova.images_and_snapshots',
#    url(r'^$', 'views.index', name='index'),
#    url(r'', include(image_urls, namespace='images')),
#    url(r'', include(snapshot_urls, namespace='snapshots')),
#)
#KDS: new code
#from django.conf.urls.defaults import *

#urlpatterns = patterns('horizon.dashboards.nova.xstream_cloud_platform',
#    url(r'^$', 'views.index', name='index'),
#)
from django.conf.urls.defaults import *

import horizon

from horizon.dashboards.nova.xstream_cloud_platform.images import urls\
                                                         as image_urls
from horizon.dashboards.nova.xstream_cloud_platform.snapshots import urls\
                                                            as snapshot_urls

urlpatterns = patterns('horizon.dashboards.nova.xstream_cloud_platform',
    url(r'^$', 'views.index', name='index'),
    url(r'', include(image_urls, namespace='images')),
    url(r'', include(snapshot_urls, namespace='snapshots')),
)
