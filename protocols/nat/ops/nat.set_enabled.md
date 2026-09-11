# nat.set_enabled

Enable or disable NAT hole-punching on the node. The value is stored as a node setting; when disabled, the node stops participating in traversal. The operation always accepts and acknowledges.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The query is rejected before the setting changes when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* arg (bool) – Whether hole-punching should be enabled. Defaults to false.

## Returned objects

The operation returns an `ack` object once the setting has been applied.

## Examples

```shellsession
$ astral-query nat.set_enabled -arg true -out json
{"Type":"ack","Object":null}
```
