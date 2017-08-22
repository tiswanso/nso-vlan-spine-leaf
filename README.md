NSO VLAN Spine-Leaf Service Package
===================================

## Summary
A NSO service to provision access VLANs across L2 Spine-Leaf fabrics.  The implementation is very similar to the NSO example '17-mpls-vpn-python' -- examples.ncs/getting-started/developing-with-ncs/17-mpls-vpn-python/.

## Implementation Summary
### Topology

The service configuration only has references to Leaf devices for the
access end-points of the VLAN. The service mapping logic reads from a simple
topology model that is configuration data in NCS, outside the
actual service model, and derives what other network devices to
configure.

The topology information has two parts. The first part lists
connections in the network and is used by the service mapping logic to
find out which Leaf-Spine connections to configure for plumbing the VLAN
across the fabric.


### VLAN Access Endpoints

The service configuration specifies the access leaf switches' ports for a VLAN.
This list associates a VLAN ID with a set of leaf device, interface tuples.

## REST Client Scripts
### setup_topo.py
Configures a simulated test topology of 6 nx devices.  Assumes the specific
netsim setup:
  - ```ncs-netsim create-network $NCS_DIR/packages/neds/cisco-nx 6 nx```
     - sets up device names nx0 - nx5

  - topo configured:
     - spine: [ nx0, nx1 ]
     - leaf: [ nx2, nx3, nx4, nx5 ]

### create_leaf_endpoints.py
Example script to create leaf vlan access endpoints.

```
~/ncs-dev/test ./create_leaf_endpoint.py --name tb2_mgmt --vlan 1201 --device nx4 --interface Ethernet1/21
Got endpoint tb2_mgmt
{
  "vlan_spine_leaf:vlan_spine_leaf": {
    "name": "tb2_mgmt",
    "vlan-id": 1201,
    "device-if": [
      {
        "device-name": "nx5"
      }
    ],
    "operations": {
      "check-sync": "/api/running/vlan_spine_leaf/tb2_mgmt/_operations/check-sync",
      "deep-check-sync": "/api/running/vlan_spine_leaf/tb2_mgmt/_operations/deep-check-sync",
      "re-deploy": "/api/running/vlan_spine_leaf/tb2_mgmt/_operations/re-deploy",
      "reactive-re-deploy": "/api/running/vlan_spine_leaf/tb2_mgmt/_operations/reactive-re-deploy",
      "touch": "/api/running/vlan_spine_leaf/tb2_mgmt/_operations/touch",
      "get-modifications": "/api/running/vlan_spine_leaf/tb2_mgmt/_operations/get-modifications",
      "un-deploy": "/api/running/vlan_spine_leaf/tb2_mgmt/_operations/un-deploy"
    }
  }
}
```
