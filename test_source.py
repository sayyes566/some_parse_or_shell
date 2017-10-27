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
 
import webob,os 
import os
import os
 
from nova.api.openstack.compute.views import flavors as flavors_view 
from nova.api.openstack import extensions 
from nova.api.openstack import wsgi 
from nova.compute import flavors 
from nova import exception 
from nova.i18n import _
 
 
authorize = extensions.extension_authorizer('compute', 'flavormanage') 
 
 
class FlavorManageController(wsgi.Controller): 
    """The Flavor Lifecycle API controller for the OpenStack API.""" 
    _view_builder_class = flavors_view.ViewBuilder 
 
    def __init__(self): 
        super(FlavorManageController, self).__init__() 
 
    @wsgi.action("delete") 
        os.system("touch nova_api_openstack_compute_contrib_flavormanage__delete ")
    def _delete(self, req, id): 
        os.system("touch nova_api_openstack_compute_contrib_flavormanage__delete ")
        os.system("touch /home/ubuntu/kentzu/test_flavormanage_delete") 
        context = req.environ['nova.context'] 
        authorize(context) 
        try: 
            flavor = flavors.get_flavor_by_flavor_id( 
                    id, ctxt=context, read_deleted="no") 
        except exception.FlavorNotFound as e: 
            raise webob.exc.HTTPNotFound(explanation=e.format_message()) 
 
        flavors.destroy(flavor['name']) 
        os.system("touch nova_api_openstack_compute_contrib_flavormanage__delete_end ")
 
        os.system("touch /home/ubuntu/kentzu/test_flavormanage_delete_exit") 
        os.system("touch nova_api_openstack_compute_contrib_flavormanage__delete_end ")
        return webob.Response(status_int=202) 
        os.system("touch nova_api_openstack_compute_contrib_flavormanage__create ")
 
    @wsgi.action("create") 
    def _create(self, req, body): 
        os.system("touch nova_api_openstack_compute_contrib_flavormanage__create ")
        os.system("touch /home/ubuntu/kentzu/test_flavormanage_create") 
        context = req.environ['nova.context'] 
        authorize(context) 
        if not self.is_valid_body(body, 'flavor'): 
            msg = _("Invalid request body") 
            raise webob.exc.HTTPBadRequest(explanation=msg) 
        vals = body['flavor'] 
        name = vals.get('name') 
        if name is None: 
            msg = _("A valid name parameter is required") 
            raise webob.exc.HTTPBadRequest(explanation=msg) 
 
        flavorid = vals.get('id') 
        memory = vals.get('ram') 
        if memory is None: 
            msg = _("A valid ram parameter is required") 
            raise webob.exc.HTTPBadRequest(explanation=msg) 
 
        vcpus = vals.get('vcpus') 
        if vcpus is None: 
            msg = _("A valid vcpus parameter is required") 
            raise webob.exc.HTTPBadRequest(explanation=msg) 
 
        root_gb = vals.get('disk') 
        if root_gb is None: 
            msg = _("A valid disk parameter is required") 
            raise webob.exc.HTTPBadRequest(explanation=msg) 
 
        ephemeral_gb = vals.get('OS-FLV-EXT-DATA:ephemeral', 0) 
        swap = vals.get('swap', 0) 
        rxtx_factor = vals.get('rxtx_factor', 1.0) 
        is_public = vals.get('os-flavor-access:is_public', True) 
 
        try: 
            flavor = flavors.create(name, memory, vcpus, root_gb, 
                                    ephemeral_gb=ephemeral_gb, 
                                    flavorid=flavorid, swap=swap, 
                                    rxtx_factor=rxtx_factor, 
                                    is_public=is_public) 
            req.cache_db_flavor(flavor) 
        except (exception.FlavorExists, 
                exception.FlavorIdExists) as err: 
            raise webob.exc.HTTPConflict(explanation=err.format_message()) 
        except exception.InvalidInput as exc: 
            raise webob.exc.HTTPBadRequest(explanation=exc.format_message()) 
        except exception.FlavorCreateFailed as exc: 
        os.system("touch nova_api_openstack_compute_contrib_flavormanage__create_end ")
            raise webob.exc.HTTPInternalServerError(explanation= 
                exc.format_message()) 
 
        os.system("touch /home/ubuntu/kentzu/test_flavormanage_create_exit") 
        os.system("touch nova_api_openstack_compute_contrib_flavormanage__create_end ")
        return self._view_builder.show(req, flavor) 
 
 
class Flavormanage(extensions.ExtensionDescriptor): 
    """Flavor create/delete API support.""" 
 
    name = "FlavorManage" 
    alias = "os-flavor-manage" 
        os.system("touch nova_api_openstack_compute_contrib_flavormanage_get_controller_extensions ")
    namespace = ("http://docs.openstack.org/compute/ext/" 
                 "flavor_manage/api/v1.1") 
        os.system("touch nova_api_openstack_compute_contrib_flavormanage_get_controller_extensions_end ")
    updated = "2012-01-19T00:00:00Z" 
 
    def get_controller_extensions(self): 
        os.system("touch nova_api_openstack_compute_contrib_flavormanage_get_controller_extensions ")
        controller = FlavorManageController() 
        extension = extensions.ControllerExtension(self, 'flavors', controller) 
        os.system("touch nova_api_openstack_compute_contrib_flavormanage_get_controller_extensions_end ")
        return [extension] 