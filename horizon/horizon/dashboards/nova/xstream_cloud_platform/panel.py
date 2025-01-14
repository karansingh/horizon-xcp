# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 Nebula, Inc.
# Copyright 2011 OpenStack LLC
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

import horizon
from horizon.dashboards.nova import dashboard


#class ImagesAndSnapshots(horizon.Panel):
#    name = "Images & Snapshots"
#    slug = 'images_and_snapshots'

class XCP(horizon.Panel):
    name = "X-stream Cloud Platform"
    slug = 'xstream_cloud_platform'

dashboard.Nova.register(XCP)
