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

"""
Views for managing Nova images.
"""

import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.utils.text import normalize_newlines
from django.utils.translation import ugettext as _
from glance.common import exception as glance_exception
from openstackx.api import exceptions as api_exceptions

from horizon import api
from horizon import forms

LOG = logging.getLogger(__name__)


class UpdateImageForm(forms.SelfHandlingForm):
    image_id = forms.CharField(widget=forms.HiddenInput())
    name = forms.CharField(max_length="25", label=_("Name"))
    kernel = forms.CharField(max_length="25", label=_("Kernel ID"),
                             required=False)
    ramdisk = forms.CharField(max_length="25", label=_("Ramdisk ID"),
                              required=False)
    architecture = forms.CharField(label=_("Architecture"), required=False)
    container_format = forms.CharField(label=_("Container Format"),
                                       required=False)
    disk_format = forms.CharField(label=_("Disk Format"))

    def handle(self, request, data):
        image_id = data['image_id']
        tenant_id = request.user.tenant_id
        error_retrieving = _('Unable to retrieve image info from glance: %s'
                             % image_id)
        error_updating = _('Error updating image with id: %s' % image_id)

        try:
            image = api.image_get_meta(request, image_id)
        except glance_exception.ClientConnectionError, e:
            LOG.exception(_('Error connecting to glance'))
            messages.error(request, error_retrieving)
        except glance_exception.Error, e:
            LOG.exception(error_retrieving)
            messages.error(request, error_retrieving)

        if image.owner == request.user.tenant_id:
            try:
                meta = {
                    'is_public': True,
                    'disk_format': data['disk_format'],
                    'container_format': data['container_format'],
                    'name': data['name'],
                }
                # TODO add public flag to properties
                meta['properties'] = {}
                if data['kernel']:
                    meta['properties']['kernel_id'] = data['kernel']

                if data['ramdisk']:
                    meta['properties']['ramdisk_id'] = data['ramdisk']

                if data['architecture']:
                    meta['properties']['architecture'] = data['architecture']

                api.image_update(request, image_id, meta)
                messages.success(request, _('Image was successfully updated.'))

            except glance_exception.ClientConnectionError, e:
                LOG.exception(_('Error connecting to glance'))
                messages.error(request, error_retrieving)
            except glance_exception.Error, e:
                LOG.exception(error_updating)
                messages.error(request, error_updating)
            except:
                LOG.exception(_('Unspecified Exception in image update'))
                messages.error(request, error_updating)
            return redirect('dash_images_update', tenant_id, image_id)
        else:
            messages.info(request, _('Unable to update image. You are not its \
                                      owner.'))
            return redirect('dash_images_update', tenant_id, image_id)

#KDS: udated LaunchForm for x-stream demo
class LaunchForm(forms.SelfHandlingForm):
    name = forms.CharField(max_length=80, label=_("X-stream Server Name"))
    image_id = forms.CharField(widget=forms.HiddenInput())
    tenant_id = forms.CharField(widget=forms.HiddenInput())
#    user_data = forms.CharField(widget=forms.HiddenInput())
#    user_data = forms.CharField(widget=forms.Textarea,
#                                label=_("Application User Data"),
#                                required=False,
#                                help_text="Add all the required meta-data")
    meta_data = forms.CharField(widget=forms.Textarea,
                                label=_("Application Meta-Data"),
                                required=False,
				help_text="Add all the required meta-data")

#    print("KDS1 xcp forms.py: meta-data=%s \n" %(meta_data))
#    flavorlist = forms.CharField(widget=forms.HiddenInput())

    # make the dropdown populate when the form is loaded not when django is
    # started
    def __init__(self, *args, **kwargs):
        super(LaunchForm, self).__init__(*args, **kwargs)
        flavorlist = kwargs.get('initial', {}).get('flavorlist', [])
        self.fields['flavor'] = forms.ChoiceField(
#		widget=forms.HiddenInput(),
                choices=flavorlist,
                label=_("Flavor"),
                help_text="Size of Image to launch")
		
        keynamelist = kwargs.get('initial', {}).get('keynamelist', [])
        self.fields['key_name'] = forms.ChoiceField(choices=keynamelist,
                label=_("Key Name"),
                required=False,
                help_text="Which keypair to use for authentication")

        securitygrouplist = kwargs.get('initial', {}).get(
                                                      'securitygrouplist', [])
#        self.fields['security_groups'] = forms.MultipleChoiceField(
#                choices=securitygrouplist,
#                label=_("Security Groups"),
#                required=True,
#                initial=['default'],
#                widget=forms.SelectMultiple(
#                       attrs={'class': 'chzn-select',
#                              'style': "min-width: 200px"}),
#                help_text="Launch instance in these Security Groups")
        # setting self.fields.keyOrder seems to break validation,
        # so ordering fields manually
        field_list = (
            'name',
#            'user_data',
            'flavor',
            'key_name')
        for field in field_list[::-1]:
            self.fields.insert(0, field, self.fields.pop(field))

    def handle(self, request, data):
        image_id = data['image_id']
        tenant_id = data['tenant_id']
#	flavor = "m1.tiny"
#KDS: hack to give some valid user_data
	user_data=data['tenant_id']
	meta_data = {'input_array' : 'default_input', 'output_array' : 'default_output'}
#        print("KDS4 xcp forms.py: dataget-metadata=%s\n" %(data.get('meta_data')))
        try:
            image = api.image_get_meta(request, image_id)
            flavor = api.flavor_get(request, data['flavor'])
            api.server_create(request,
                              data['name'],
                              image,
                              flavor,
                              data.get('key_name'),
                              user_data,
			      meta_data,
#			      data.get('meta_data'),
                              data.get('security_groups'))
#KDS: pass meta_data as 'meta' instead of 'user_data'
	    print("KDS2 xcp forms.py: meta-data=%s dataget-metadata=%s\n" %(meta_data, data.get('meta_data')))
            msg = _('Instance was successfully launched')
            LOG.info(msg)
            messages.success(request, msg)
            return redirect(
                        'horizon:nova:instances_and_volumes:instances:index')

        except api_exceptions.ApiException, e:
            LOG.exception('ApiException while creating instances of image "%s"'
                           % image_id)
            messages.error(request,
                           _('Unable to launch instance: %s') % e.message)
            print("KDS3 xcp forms.py: meta-data=%s dataget-metadata=%s\n" %(meta_data, data.get('meta_data')))

class DeleteImage(forms.SelfHandlingForm):
    image_id = forms.CharField(required=True)

    def handle(self, request, data):
        image_id = data['image_id']
        tenant_id = request.user.tenant_id
        try:
            image = api.image_get_meta(request, image_id)
            if image.owner == request.user.username:
                api.image_delete(request, image_id)
            else:
                messages.info(request, _("Unable to delete image, you are not \
                                         its owner."))
                return redirect('dash_images_update', tenant_id, image_id)
        except glance_exception.ClientConnectionError, e:
            LOG.exception("Error connecting to glance")
            messages.error(request, _("Error connecting to glance: %s")
                                    % e.message)
        except glance_exception.Error, e:
            LOG.exception('Error deleting image with id "%s"' % image_id)
            messages.error(request,
                    _("Error deleting image: %(image)s: %i(msg)s")
                    % {"image": image_id, "msg": e.message})
        return redirect(request.build_absolute_uri())
