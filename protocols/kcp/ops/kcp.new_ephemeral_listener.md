# kcp.new_ephemeral_listener

Start an ephemeral KCP listener on the given UDP port. The operation fails if a listener already exists on that port.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The query is rejected before any socket is opened when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* port (uint16, required) – UDP port to listen on.

## Returned objects

The operation returns one of:
* An `error_message` object if the port is already in use or the listener cannot be started.
* An `ack` object if the listener was started successfully.

## Examples

```shellsession
$ astral-query kcp.new_ephemeral_listener -port 9000 -out json
{"Type":"ack","Object":null}
```
