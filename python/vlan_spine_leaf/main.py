# -*- mode: python; python-indent: 4 -*-
"""Prototype L2 spine-leaf setup NCS Service module.

Copyright 2016 Cisco Inc.
"""

import ncs
from ncs.application import Service

# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------
class ServiceCallbacks(Service):

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')
        self.service = service
        self.root = root
        topology = root.topology
        device_ifs = service.device_if

        self.log.debug("Topology ", topology, " device_ifs ", device_ifs)

        for dev_if in device_ifs:
            for connection in topology.connection:
                e1_dev = connection.endpoint_1.device
                e2_dev = connection.endpoint_2.device
                leaf_name = dev_if.device_name
                if (e1_dev == leaf_name) or (e2_dev == leaf_name):
                    # setup VLAN for connection
                    self.setup_connection(connection)
            # setup the connection out of the leaf
            self.setup_vlan_on_intf(dev_if.device_name, dev_if.interface)

    # The pre_modification() and post_modification() callbacks are optional,
    # and are invoked outside FASTMAP. pre_modification() is invoked before
    # create, update, or delete of the service, as indicated by the enum
    # ncs_service_operation op parameter. Conversely
    # post_modification() is invoked after create, update, or delete
    # of the service. These functions can be useful e.g. for
    # allocations that should be stored and existing also when the
    # service instance is removed.

    # @Service.pre_lock_create
    # def cb_pre_lock_create(self, tctx, root, service, proplist):
    #     self.log.info('Service plcreate(service=', service._path, ')')

    # @Service.pre_modification
    # def cb_pre_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')

    # @Service.post_modification
    # def cb_post_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')

    def setup_vlan_on_intf(self, device, interface):
        """Provisions VLAN on a device's interface"""
        tv = ncs.template.Variables()
        tv.add('DEV', device)
        tv.add('INTERFACE', interface)
        tmpl = ncs.template.Template(self.service)
        tmpl.apply('vlan', tv)

    def setup_connection(self, conn):
        """Provisions each interface in connection"""
        self.setup_vlan_on_intf(conn.endpoint_1.device,
                                conn.endpoint_1.interface)
        self.setup_vlan_on_intf(conn.endpoint_2.device,
                                conn.endpoint_2.interface)


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('vlan_spine_leaf-servicepoint', ServiceCallbacks)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
