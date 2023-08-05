# Hydraulic Network Client Library

This library allows connections to remote hydraulic network REST servers. It
supports authentication with OpenID Connect.

## Installation

Install with `pip`:

```bash
> python -m pip install kisters.water.hydraulic_network.client
```


## Example Usage

### Create Client

```python
from kisters.water.hydraulic_network.client import (
    OpenIDConnect,  # provides authentication tokens for the client
    RESTClient,  # communicates with a network store service
)

# Instantiate the authentication class with credentials
authentication = OpenIDConnect(
    issuer_url="https://auth.kisters.cloud/auth/realms/external",
    client_id="jesse-test",
    client_secret="c4b0f70d-d2e6-497f-b11c-d49fe806c29b",
)
# Instantiate the client class with the service url and authentication
client = RESTClient(
    url="https://jesse-test.hydraulic-network.kisters.cloud/",
    authentication=authentication
)
# Verify the client is set up correctly
# Note: If you have not created any networks yet, this could be an empty list
client.get(("rest", "networks"))
# ['my-network', 'my-other-network', ...]
```

### Connect to a Network

```python
from kisters.water.hydraulic_network.client import Network

# Instantiate the Network class with the network name and client
network = Network("my-network", client)

# You can now access the properties of the network
network.get_nodes()
# [
# FlowBoundary(
#     created=datetime.datetime(2019, 6, 27, 16, 53, 5),
#     uid='flow_boundary',
#     display_name='flow_boundary',
#     location={'x': 0.0, 'y': 0.0, 'z': 0.0},
#     schematic_location={'x': 0.0, 'y': 0.0, 'z': 0.0})
# ,
# ...
# ]
```