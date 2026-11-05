# nearby.broadcast

Triggers an immediate broadcast of the local node's status to nearby peers. The op is a no-op when the module is in silent mode. A node without an active contract acts in visible mode unless its stored mode is silent ([mod.nearby.mode](../types/mod.nearby.mode.md)).

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The operation answers an `error_message` reading `not permitted` before any
status is broadcast when the caller is not authorized.

## Arguments

* out (string, optional) – Output encoding format. Defaults to the channel default.

## Returned objects

The operation returns one of:
* An `error_message` object if the broadcast fails.
* An `ack` object on success.

## Examples

```shellsession
$ astral-query nearby.broadcast -out json
{"Type":"ack","Object":null}
```
