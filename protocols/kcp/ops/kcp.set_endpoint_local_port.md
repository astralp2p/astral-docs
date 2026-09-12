# kcp.set_endpoint_local_port

Map a remote KCP endpoint to a local UDP port. The query is rejected immediately if `endpoint` cannot be parsed; otherwise the operation fails if a mapping already exists and `replace` is false.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The query is rejected before `endpoint` is parsed or any mapping changes when
the caller is not authorized, and a refused caller receives no bytes.

## Arguments

* endpoint (string, required) – Remote KCP endpoint in `host:port` form.
* local_port (uint16, required) – Local UDP port to map the endpoint to.
* replace (bool) – When true, an existing mapping for the endpoint is replaced. Defaults to false.

## Returned objects

The operation returns one of:
* An `error_message` object if the mapping already exists (and `replace` is false) or the mapping cannot be set.
* An `ack` object if the mapping was set successfully.

## Examples

```shellsession
$ astral-query kcp.set_endpoint_local_port -endpoint 203.0.113.10:7000 -local_port 8000 -out json
{"Type":"ack","Object":null}
```
