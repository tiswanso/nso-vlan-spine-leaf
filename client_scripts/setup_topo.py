#!/usr/bin/env python
from collections import OrderedDict
import json
import requests

# Sets up vlan_spine_leaf topology config in NSO for specific ncs-netsim network
#
# NOTE: for now assumes:
#  - simulation setup 
#    ncs-netsim create-network $NCS_DIR/packages/neds/cisco-nx 6 nx
#     (device names nx0 - nx5)
#
#  - topo:
#      spine: [ nx0, nx1 ]
#      leaf: [ nx2, nx3, nx4, nx5 ]
#

spines = [ 'nx0', 'nx1' ]
leafs = [ 'nx2', 'nx3', 'nx4', 'nx5' ]
roles = { 'spine': spines, 'leaf': leafs }

intf_start = { 'leaf': 2, 'spine': 10 }

dev_intfs = {}

HEADERS = {'Content-type': 'application/vnd.yang.data+json', 'Accept': 'application/vnd.yang.data+json'}
conn_base_url = "http://localhost:8080/api/running/topology/connection"
role_base_url = "http://localhost:8080/api/running/topology/role"
ncs_username = 'admin'
ncs_password = 'admin'
ncs_auth = requests.auth.HTTPBasicAuth(ncs_username, ncs_password)

def get_next_intf(node, role):
    if not node in dev_intfs:
        dev_intfs[node] = intf_start[role]

    intf_num = dev_intfs[node]
    dev_intfs[node] += 1

    return intf_num

def create_connection(name, conn_payload_d):
    # Use 'PUT', 'POST' doesn't seem to work to create
    resp = requests.put(conn_base_url + "/" + name,
                        data=json.dumps({"vlan_spine_leaf:connection": conn_payload_d}),
                        auth=ncs_auth,
                        headers=HEADERS)
    if resp.status_code < 200 or resp.status_code > 299:
        print "ERROR: creating connection {name}: {txt}".format(name=name,
                                                                txt=resp.text)
    else:
        print "Created connection {name}".format(name=name) 

def setup_connections():
    for leaf in leafs:
        for spine in spines:
            con_name = "{s}_{l}".format(l=leaf, s=spine)
            print "setting up connection: " + con_name
            s_int = get_next_intf(spine, 'spine')
            conn_payload_d = OrderedDict()
            conn_payload_d['name'] = con_name
            conn_payload_d['endpoint-1'] = {
                'device': spine,
                'interface': "Ethernet1/{id}".format(id=s_int)
                }
            l_int = get_next_intf(leaf, 'leaf')
            conn_payload_d['endpoint-2'] = {
                'device': leaf,
                'interface': "Ethernet1/{id}".format(id=l_int)
                }
            create_connection(con_name, conn_payload_d)

def setup_role(role, role_payload_d):
    # 'POST' doesn't work to create
    resp = requests.put(role_base_url + "/" + role,
                        data=json.dumps({"vlan_spine_leaf:role": role_payload_d}),
                        auth=ncs_auth,
                        headers=HEADERS)
    if resp.status_code < 200 or resp.status_code > 299:
        print "ERROR: creating role {name}: {txt}".format(name=role,
                                                      txt=resp.text)
    else:
        print "Created role {name}".format(name=role) 

def setup_roles():
    for role in roles:
        # Use OrderedDict for REST payload.
        # NCS requires the list key to be first item in json dict.
        role_payload_d = OrderedDict()
        role_payload_d['role'] = role
        role_payload_d['device'] = roles[role]
        setup_role(role, role_payload_d)

def main():
    setup_roles()
    setup_connections()

if __name__ == '__main__':
    main()
