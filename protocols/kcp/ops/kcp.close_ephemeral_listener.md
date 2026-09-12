# kcp.close_ephemeral_listener

Stop an ephemeral KCP listener running on the given UDP port. The operation fails if no ephemeral listener exists on that port.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The query is rejected before any listener is closed when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* port (uint16, required) – UDP port of the listener to close.

## Returned objects

The operation returns one of:
* An `error_message` object if the listener does not exist or cannot be closed.
* An `ack` object if the listener was stopped successfully.

## Examples

```shellsession
$ astral-query kcp.close_ephemeral_listener -port 9000 -out json
{"Type":"ack","Object":null}
```
