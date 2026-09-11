# kcp.remove_endpoint_local_port

Remove the local UDP port mapping for a remote KCP endpoint. The query is rejected immediately if `endpoint` cannot be parsed.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The query is rejected before `endpoint` is parsed or any mapping changes when
the caller is not authorized, and a refused caller receives no bytes.

## Arguments

* endpoint (string8, required) – Remote KCP endpoint in `host:port` form.

## Returned objects

The operation returns one of:
* An `error_message` object if the mapping does not exist or cannot be removed.
* An `ack` object if the mapping was removed successfully.

## Examples

```shellsession
$ astral-query kcp.remove_endpoint_local_port -endpoint 203.0.113.10:7000 -out json
{"Type":"ack","Object":null}
```
