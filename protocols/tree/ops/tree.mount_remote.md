# tree.mount_remote

Mount a remote node's tree subtree at a local path.

The caller must hold
[`mod.auth.configure_node_state_action`](../../auth/types/mod.auth.configure_node_state_action.md).
The query is rejected before the target is resolved or the remote tree is
queried when the caller is not authorized, and a refused caller receives no
bytes.

## Arguments

* path (string8, required) – The local path at which to mount the remote subtree.
* target (string8, required) – The identity (or alias) of the remote node to mount from.
* root (string8) – The path on the remote node to use as the root of the mount. Defaults to `/` if omitted.

## Returned objects

The operation returns one of:
* An `error_message` object if there was an error.
* An `ack` object if the mount was established successfully.

## Examples

```shellsession
$ astral-query tree.mount_remote -path /remote/peer -target somenode -root /mod -out json
{"Type":"ack","Object":null}
```
