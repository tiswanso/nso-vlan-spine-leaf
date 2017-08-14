#!/usr/bin/env python
import argparse
from collections import OrderedDict
import json
import requests
import yaml

HEADERS = {'Content-type': 'application/vnd.yang.data+json', 'Accept': 'application/vnd.yang.data+json'}
ncs_username = 'admin'
ncs_password = 'admin'
ncs_auth = requests.auth.HTTPBasicAuth(ncs_username, ncs_password)

vsl_base_url = "http://localhost:8080/api/running/vlan_spine_leaf"

def check_endpoint(name):
    resp = requests.get(vsl_base_url + "/" + name,
                        auth=ncs_auth, headers=HEADERS)
    if resp.status_code < 200 or resp.status_code > 299:
        print "ERROR: getting endpoint {name}: {txt}".format(name=name,
                                                             txt=resp.text)
        return False
    else:
        print "Got endpoint {name}".format(name=name)
        print resp.text
    return True


def update_endpoint(name, vlan, device, interface):
    vsl_payload_d = OrderedDict()
    vsl_payload_d['name'] = name
    vsl_payload_d['vlan-id'] = vlan
    vsl_payload_d['device-if'] = OrderedDict()
    vsl_payload_d['device-if']['device-name'] = device
    vsl_payload_d['device-if']['interface'] = interface
    resp = requests.patch(vsl_base_url + "/" + name,
                          data=json.dumps({ "vlan_spine_leaf:vlan_spine_leaf": vsl_payload_d}),
                          auth=ncs_auth, headers=HEADERS)
    if resp.status_code < 200 or resp.status_code > 299:
        print "ERROR: Updating endpoint {name}: {txt}".format(name=name,
                                                              txt=resp.text)
    else:
        print "Updated endpoint {name}".format(name=name)


def create_endpoint(name, vlan, device, interface):
    vsl_payload_d = OrderedDict()
    vsl_payload_d['name'] = name
    vsl_payload_d['vlan-id'] = vlan
    vsl_payload_d['device-if'] = OrderedDict()
    vsl_payload_d['device-if']['device-name'] = device
    vsl_payload_d['device-if']['interface'] = interface
    resp = requests.put(vsl_base_url + "/" + name,
                        data=json.dumps({ "vlan_spine_leaf:vlan_spine_leaf": vsl_payload_d}),
                        auth=ncs_auth, headers=HEADERS)
    if resp.status_code < 200 or resp.status_code > 299:
        print "ERROR: creating endpoint {name}: {txt}".format(name=name,
                                                              txt=resp.text)
    else:
        print "Created endpoint {name}".format(name=name)


def main():
    parser = argparse.ArgumentParser(description='Utility to create VLAN endpoints on leaf access ports.')
    parser.add_argument('--name',
                        help='Name of endpoint.')

    parser.add_argument('--vlan', type=int, choices=xrange(1, 4096),
                        help='vlan ID for the endpoint.')

    parser.add_argument('--device',
                        help='Device name of the access leaf.')

    parser.add_argument('--interface',
                        help='Access interface of the leaf endpoint.')

    args = parser.parse_args()

    if check_endpoint(args.name):
        update_endpoint(args.name, args.vlan, args.device, args.interface)
    else:
        create_endpoint(args.name, args.vlan, args.device, args.interface)

if __name__ == '__main__':
    main()
