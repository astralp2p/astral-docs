# kcp.remove_endpoint_local_port

Remove the local UDP port mapping for a remote KCP endpoint. The query is rejected immediately if `endpoint` cannot be parsed.

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
