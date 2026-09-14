# tree.mount_remote

Mount a remote node's tree subtree at a local path.

The caller must hold
[`mod.auth.configure_node_state_action`](../../auth/types/mod.auth.configure_node_state_action.md).
The query is rejected before the target is resolved or the remote tree is
queried when the caller is not authorized, and a refused caller receives no
bytes.

The mount queries the target as the mounting node's own identity, not as the
caller and not as the user. The target answers under its own rules. A node
member of the target's swarm holds
[`mod.auth.see_node_state_action`](../../auth/types/mod.auth.see_node_state_action.md)
and reads the mounted tree. Writing through the mount answers to
[`mod.auth.configure_node_state_action`](../../auth/types/mod.auth.configure_node_state_action.md)
on the target, which no swarm membership grants: the target records a node-local
grant for the mounting node, or a signed contract carries it.

The operation queries the target before it records the mount point, with `root`
given and without it. A target that refuses the query, or does not answer it,
fails the operation and no mount is recorded.

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
