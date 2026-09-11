# kcp.list_endpoint_local_mappings

Stream all current remote-endpoint-to-local-port mappings. The operation emits one `mod.kcp.endpoint_local_mapping` object per mapping, then terminates with `eos`.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The query is rejected before any mapping is read when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

No arguments.

## Returned objects

The operation returns one of:
* A `mod.kcp.endpoint_local_mapping` object for each stored mapping.
* An `error_message` object if sending a mapping fails.
* An `eos` object terminating the stream.

## Examples

```shellsession
$ astral-query kcp.list_endpoint_local_mappings -out json
{"Type":"mod.kcp.endpoint_local_mapping","Object":{"Address":"203.0.113.10:7000","Port":8000}}
{"Type":"eos","Object":null}
```
