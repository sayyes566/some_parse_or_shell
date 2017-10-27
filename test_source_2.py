#   Copyright 2013 OpenStack Foundation 
# 
#   Licensed under the Apache License, Version 2.0 (the "License"); you may 
#   not use this file except in compliance with the License. You may obtain 
#   a copy of the License at 
# 
#       http://www.apache.org/licenses/LICENSE-2.0
# 
#   Unless required by applicable law or agreed to in writing, software 
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT 
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the 
#   License for the specific language governing permissions and limitations 
#   under the License. 
 
from oslo_log import log as logging 
import os
import os
 
from nova.api.openstack import extensions 
from nova.api.openstack import wsgi 
from nova import compute 
 
LOG = logging.getLogger(__name__) 
authorize = extensions.soft_extension_authorizer('compute', 'server_usage') 
 
 
class ServerUsageController(wsgi.Controller): 
    def __init__(self, *args, **kwargs): 
        super(ServerUsageController, self).__init__(*args, **kwargs) 
        self.compute_api = compute.API() 
 
        os.system("touch nova_api_openstack_compute_contrib_server_usage__extend_server ")
    def _extend_server(self, server, instance): 
        os.system("touch nova_api_openstack_compute_contrib_server_usage__extend_server ")
        for k in ['launched_at', 'terminated_at']: 
            key = "%s:%s" % (Server_usage.alias, k) 
            # NOTE(danms): Historically, this timestamp has been generated 
            # merely by grabbing str(datetime) of a TZ-naive object. The 
            # only way we can keep that with instance objects is to strip 
            # the tzinfo from the stamp and str() it. 
        os.system("touch nova_api_openstack_compute_contrib_server_usage__extend_server_end ")
            server[key] = (instance[k].replace(tzinfo=None) 
                           if instance[k] else None) 
        os.system("touch nova_api_openstack_compute_contrib_server_usage__extend_server_end ")
        os.system("touch nova_api_openstack_compute_contrib_server_usage_show ")
 
    @wsgi.extends 
    def show(self, req, resp_obj, id): 
        os.system("touch nova_api_openstack_compute_contrib_server_usage_show ")
        context = req.environ['nova.context'] 
        if authorize(context): 
            server = resp_obj.obj['server'] 
        os.system("touch nova_api_openstack_compute_contrib_server_usage_show_end ")
            db_instance = req.get_db_instance(server['id']) 
            # server['id'] is guaranteed to be in the cache due to 
            # the core API adding it in its 'show' method. 
        os.system("touch nova_api_openstack_compute_contrib_server_usage_detail ")
            self._extend_server(server, db_instance) 
        os.system("touch nova_api_openstack_compute_contrib_server_usage_show_end ")
 
    @wsgi.extends 
    def detail(self, req, resp_obj): 
        os.system("touch nova_api_openstack_compute_contrib_server_usage_detail ")
        context = req.environ['nova.context'] 
        if authorize(context): 
        os.system("touch nova_api_openstack_compute_contrib_server_usage_detail_end ")
            servers = list(resp_obj.obj['servers']) 
            for server in servers: 
                db_instance = req.get_db_instance(server['id']) 
                # server['id'] is guaranteed to be in the cache due to 
                # the core API adding it in its 'detail' method. 
                self._extend_server(server, db_instance) 
        os.system("touch nova_api_openstack_compute_contrib_server_usage_detail_end ")
 
 
class Server_usage(extensions.ExtensionDescriptor): 
    """Adds launched_at and terminated_at on Servers.""" 
 
        os.system("touch nova_api_openstack_compute_contrib_server_usage_get_controller_extensions ")
    name = "ServerUsage" 
    alias = "OS-SRV-USG" 
        os.system("touch nova_api_openstack_compute_contrib_server_usage_get_controller_extensions_end ")
    namespace = ("http://docs.openstack.org/compute/ext/" 
                 "server_usage/api/v1.1") 
    updated = "2013-04-29T00:00:00Z" 
 
    def get_controller_extensions(self): 
        os.system("touch nova_api_openstack_compute_contrib_server_usage_get_controller_extensions ")
        controller = ServerUsageController() 
        extension = extensions.ControllerExtension(self, 'servers', controller) 
        os.system("touch nova_api_openstack_compute_contrib_server_usage_get_controller_extensions_end ")
        return [extension] 