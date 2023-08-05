# Piksel Netbox
> Python Module for automating the creation, deletion and maintenance of IPAM objects.

## Usage
Install with pip
```
pip3 install pikselnetbox
```

```
from pikselnetbox import pikselnetbox
import socket

netbox = pikselnetbox.Helper(NETBOX TOKEN, NETBOX_URL)
interfaces = netbox.get_interface_ips()

for interface in interfaces:
    get_ip = netbox.get_ipam_object(interface)

print(get_ip[0])
```
