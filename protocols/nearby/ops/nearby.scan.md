# nearby.scan

Broadcasts a [`mod.nearby.scan_message`](../types/mod.nearby.scan_message.md) on every local IPv4 subnet, asking the nodes there to broadcast their status. Each node in mode `1` (Visible) or `2` (Stealth) answers on the subnet the scan came from, at once or at the end of its 2-second reply window. The op answers before any reply arrives; [`nearby.list`](nearby.list.md) shows the statuses received. In mode `0` (Silent) the node sends nothing and answers `ack`.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The operation answers an `error_message` reading `not permitted` before any
scan is sent when the caller is not authorized.

## Arguments

This operation takes no arguments.

## Returned objects

The operation returns one of:
* An `error_message` object if the scan fails.
* An `ack` object on success, and in mode `0` (Silent).

## Examples

```shellsession
$ astral-query nearby.scan -out json
{"Type":"ack","Object":null}
```
