# tree.unmount

Unmount a previously mounted remote subtree from a local path.

The caller must hold
[`mod.auth.configure_node_state_action`](../../auth/types/mod.auth.configure_node_state_action.md).
The query is rejected before any mount is removed when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* path (string8, required) – The local path to unmount.

## Returned objects

The operation returns one of:
* An `error_message` object if the path is not mounted or there was an error.
* An `ack` object if the unmount was successful.

## Examples

```shellsession
$ astral-query tree.unmount -path /remote/peer -out json
{"Type":"ack","Object":null}
```
