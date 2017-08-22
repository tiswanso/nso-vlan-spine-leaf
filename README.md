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

Examples
--------
### Setup and Usage with Simulated Devices

**Start NCS with 6 node cisco-nx simulated net**

```
~ mkdir ncs-demo
~ cd ncs-demo
~/ncs-demo source ~/ncs-4.4.2.1/ncsrc
~/ncs-demo ncs-netsim create-network $NCS_DIR/packages/neds/cisco-nx 6 nx
DEVICE nx0 CREATED
DEVICE nx1 CREATED
DEVICE nx2 CREATED
DEVICE nx3 CREATED
DEVICE nx4 CREATED
DEVICE nx5 CREATED
~/ncs-demo ncs-netsim start
DEVICE nx0 OK STARTED
DEVICE nx1 OK STARTED
DEVICE nx2 OK STARTED
DEVICE nx3 OK STARTED
DEVICE nx4 OK STARTED
DEVICE nx5 OK STARTED
~/ncs-demo ncs-setup --netsim-dir ./netsim --dest . --package cisco-ios --package cisco-nx --package ../ncs-dev/packages/vlan_spine_leaf
Using netsim dir ./netsim
~/ncs-demo ncs
~/ncs-demo ncs_cli -u admin

admin connected from 127.0.0.1 using console on TISWANSO-M-W0TB
admin@ncs> show configuration vlan_spine_leaf 
No entries found.
[ok][2017-08-22 16:32:10]
admin@ncs> show devices brief
NAME  ADDRESS    DESCRIPTION  NED ID    
--------------------------------------
nx0   127.0.0.1  -            cisco-nx  
nx1   127.0.0.1  -            cisco-nx  
nx2   127.0.0.1  -            cisco-nx  
nx3   127.0.0.1  -            cisco-nx  
nx4   127.0.0.1  -            cisco-nx  
nx5   127.0.0.1  -            cisco-nx  
[ok][2017-08-22 16:46:09]
dmin@ncs> request devices connect
connect-result {
    device nx0
    result true
    info (admin) Connected to nx0 - 127.0.0.1:10022
}
connect-result {
    device nx1
    result true
    info (admin) Connected to nx1 - 127.0.0.1:10023
}
connect-result {
    device nx2
    result true
    info (admin) Connected to nx2 - 127.0.0.1:10024
}
connect-result {
    device nx3
    result true
    info (admin) Connected to nx3 - 127.0.0.1:10025
}
connect-result {
    device nx4
    result true
    info (admin) Connected to nx4 - 127.0.0.1:10026
}
connect-result {
    device nx5
    result true
    info (admin) Connected to nx5 - 127.0.0.1:10027
}
[ok][2017-08-22 16:46:50]
admin@ncs> request devices sync-from
sync-result {
    device nx0
    result true
}
sync-result {
    device nx1
    result true
}
sync-result {
    device nx2
    result true
}
sync-result {
    device nx3
    result true
}
sync-result {
    device nx4
    result true
}
sync-result {
    device nx5
    result true
}
[ok][2017-08-22 16:47:02]
```

**Setup topology with nx0, nx1 as spine switches**

```
~/ncs-dev/packages/vlan_spine_leaf/client_scripts(master ✔) ./setup_topo.py     
Created role spine
Created role leaf
setting up connection: nx0_nx2
Created connection nx0_nx2
setting up connection: nx1_nx2
Created connection nx1_nx2
setting up connection: nx0_nx3
Created connection nx0_nx3
setting up connection: nx1_nx3
Created connection nx1_nx3
setting up connection: nx0_nx4
Created connection nx0_nx4
setting up connection: nx1_nx4
Created connection nx1_nx4
setting up connection: nx0_nx5
Created connection nx0_nx5
setting up connection: nx1_nx5
Created connection nx1_nx5
```

See topology setup in NSO CLI
```
admin@ncs> show configuration topology 
role spine {
    device [ nx0 nx1 ];
}
role leaf {
    device [ nx2 nx3 nx4 nx5 ];
}
connection nx0_nx2 {
    endpoint-1 {
        device    nx0;
        interface Ethernet1/10;
    }
    endpoint-2 {
        device    nx2;
        interface Ethernet1/2;
    }
}
connection nx0_nx3 {
    endpoint-1 {
        device    nx0;
        interface Ethernet1/11;
    }
    endpoint-2 {
        device    nx3;
        interface Ethernet1/2;
    }
}
connection nx0_nx4 {
    endpoint-1 {
        device    nx0;
        interface Ethernet1/12;
    }
    endpoint-2 {
        device    nx4;
        interface Ethernet1/2;
    }
}
connection nx0_nx5 {
    endpoint-1 {
        device    nx0;
        interface Ethernet1/13;
    }
    endpoint-2 {
        device    nx5;
        interface Ethernet1/2;
    }
}
connection nx1_nx2 {
    endpoint-1 {
        device    nx1;
        interface Ethernet1/10;
    }
    endpoint-2 {
        device    nx2;
        interface Ethernet1/3;
    }
}
connection nx1_nx3 {
    endpoint-1 {
        device    nx1;
        interface Ethernet1/11;
    }
    endpoint-2 {
        device    nx3;
        interface Ethernet1/3;
    }
}
connection nx1_nx4 {
    endpoint-1 {
        device    nx1;
        interface Ethernet1/12;
    }
    endpoint-2 {
        device    nx4;
        interface Ethernet1/3;
    }
}
connection nx1_nx5 {
    endpoint-1 {
        device    nx1;
        interface Ethernet1/13;
    }
    endpoint-2 {
        device    nx5;
        interface Ethernet1/3;
    }
}
[ok][2017-08-22 17:00:27]
```

**Create/Add VLANs to Leaf Access Switchports**
```
~/ncs-dev/packages/vlan_spine_leaf/client_scripts(master ✗) ./create_leaf_endpoint.py --name tb2_mgmt --vlan 1201 --device nx4 --interface Ethernet1/21
ERROR: getting endpoint tb2_mgmt: 
Created endpoint tb2_mgmt
~/ncs-dev/packages/vlan_spine_leaf/client_scripts(master ✗) ./create_leaf_endpoint.py --name tb1_mgmt --vlan 1200 --device nx2 --interface Ethernet1/20
ERROR: getting endpoint tb1_mgmt: 
Created endpoint tb1_mgmt
~/ncs-dev/packages/vlan_spine_leaf/client_scripts(master ✗) ./create_leaf_endpoint.py --name tb1_mgmt --vlan 1200 --device nx4 --interface Ethernet1/20
Got endpoint tb1_mgmt
{
  "vlan_spine_leaf:vlan_spine_leaf": {
    "name": "tb1_mgmt",
    "vlan-id": 1200,
    "device-if": [
      {
        "device-name": "nx2"
      }
    ],
    "operations": {
      "check-sync": "/api/running/vlan_spine_leaf/tb1_mgmt/_operations/check-sync",
      "deep-check-sync": "/api/running/vlan_spine_leaf/tb1_mgmt/_operations/deep-check-sync",
      "re-deploy": "/api/running/vlan_spine_leaf/tb1_mgmt/_operations/re-deploy",
      "reactive-re-deploy": "/api/running/vlan_spine_leaf/tb1_mgmt/_operations/reactive-re-deploy",
      "touch": "/api/running/vlan_spine_leaf/tb1_mgmt/_operations/touch",
      "get-modifications": "/api/running/vlan_spine_leaf/tb1_mgmt/_operations/get-modifications",
      "un-deploy": "/api/running/vlan_spine_leaf/tb1_mgmt/_operations/un-deploy"
    }
  }
}

Updated endpoint tb1_mgmt
~/ncs-dev/packages/vlan_spine_leaf/client_scripts(master ✗) ./create_leaf_endpoint.py --name tb1_mgmt --vlan 1200 --device nx5 --interface Ethernet1/20
Got endpoint tb1_mgmt
{
  "vlan_spine_leaf:vlan_spine_leaf": {
    "name": "tb1_mgmt",
    "vlan-id": 1200,
    "device-if": [
      {
        "device-name": "nx2"
      },
      {
        "device-name": "nx4"
      }
    ],
    "operations": {
      "check-sync": "/api/running/vlan_spine_leaf/tb1_mgmt/_operations/check-sync",
      "deep-check-sync": "/api/running/vlan_spine_leaf/tb1_mgmt/_operations/deep-check-sync",
      "re-deploy": "/api/running/vlan_spine_leaf/tb1_mgmt/_operations/re-deploy",
      "reactive-re-deploy": "/api/running/vlan_spine_leaf/tb1_mgmt/_operations/reactive-re-deploy",
      "touch": "/api/running/vlan_spine_leaf/tb1_mgmt/_operations/touch",
      "get-modifications": "/api/running/vlan_spine_leaf/tb1_mgmt/_operations/get-modifications",
      "un-deploy": "/api/running/vlan_spine_leaf/tb1_mgmt/_operations/un-deploy"
    }
  }
}

Updated endpoint tb1_mgmt
~/ncs-dev/packages/vlan_spine_leaf/client_scripts(master ✗) ./create_leaf_endpoint.py --name tb1_stor --vlan 900 --device nx4 --interface Ethernet1/21
ERROR: getting endpoint tb1_stor: 
Created endpoint tb1_stor
~/ncs-dev/packages/vlan_spine_leaf/client_scripts(master ✗) ./create_leaf_endpoint.py --name tb1_stor --vlan 900 --device nx5 --interface Ethernet1/21
Got endpoint tb1_stor
{
  "vlan_spine_leaf:vlan_spine_leaf": {
    "name": "tb1_stor",
    "vlan-id": 900,
    "device-if": [
      {
        "device-name": "nx4"
      }
    ],
    "operations": {
      "check-sync": "/api/running/vlan_spine_leaf/tb1_stor/_operations/check-sync",
      "deep-check-sync": "/api/running/vlan_spine_leaf/tb1_stor/_operations/deep-check-sync",
      "re-deploy": "/api/running/vlan_spine_leaf/tb1_stor/_operations/re-deploy",
      "reactive-re-deploy": "/api/running/vlan_spine_leaf/tb1_stor/_operations/reactive-re-deploy",
      "touch": "/api/running/vlan_spine_leaf/tb1_stor/_operations/touch",
      "get-modifications": "/api/running/vlan_spine_leaf/tb1_stor/_operations/get-modifications",
      "un-deploy": "/api/running/vlan_spine_leaf/tb1_stor/_operations/un-deploy"
    }
  }
}

Updated endpoint tb1_stor
~/ncs-dev/packages/vlan_spine_leaf/client_scripts(master ✗) ./create_leaf_endpoint.py --name tb2_mgmt --vlan 1201 --device nx5 --interface Ethernet1/21
Got endpoint tb2_mgmt
{
  "vlan_spine_leaf:vlan_spine_leaf": {
    "name": "tb2_mgmt",
    "vlan-id": 1201,
    "device-if": [
      {
        "device-name": "nx4"
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

Updated endpoint tb2_mgmt
```

**Show vlan_spine_leaf configuration**

```
admin@ncs> show configuration vlan_spine_leaf 
vlan_spine_leaf tb1_mgmt {
    vlan-id 1200;
    device-if nx2 {
        interface Ethernet1/20;
    }
    device-if nx4 {
        interface Ethernet1/20;
    }
    device-if nx5 {
        interface Ethernet1/20;
    }
}
vlan_spine_leaf tb1_stor {
    vlan-id 900;
    device-if nx4 {
        interface Ethernet1/21;
    }
    device-if nx5 {
        interface Ethernet1/21;
    }
}
vlan_spine_leaf tb2_mgmt {
    vlan-id 1201;
    device-if nx4 {
        interface Ethernet1/21;
    }
    device-if nx5 {
        interface Ethernet1/21;
    }
}
```

**Show the device level configuration**

NOTE: The following configuration is shown right after the first access interface on leaf nx4 was created via: ```./create_leaf_endpoint.py --name tb2_mgmt --vlan 1201 --device nx4 --interface Ethernet1/21```

```
admin@ncs> show configuration devices device nx4 config nx:vlan                   
vlan-list 1;
vlan-list 380;
vlan-list 400;
vlan-list 1201;
[ok][2017-08-22 17:26:51]
admin@ncs> show configuration devices device nx4 config nx:interface Ethernet 1/2     
switchport {
    mode trunk;
    trunk {
        allowed {
            vlan {
                ids [ 1201 ];
            }
        }
    }
}
[ok][2017-08-22 17:25:05]
admin@ncs> show configuration devices device nx4 config nx:interface Ethernet 1/3
switchport {
    mode trunk;
    trunk {
        allowed {
            vlan {
                ids [ 1201 ];
            }
        }
    }
}
[ok][2017-08-22 17:25:07]
admin@ncs> show configuration devices device nx4 config nx:interface Ethernet 1/21
switchport {
    mode trunk;
    trunk {
        allowed {
            vlan {
                ids [ 1201 ];
            }
        }
    }
}
[ok][2017-08-22 17:25:22]

```