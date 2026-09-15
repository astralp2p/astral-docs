# tree.mount_remote

Mount a remote node's tree subtree at a local path.

The caller must hold
[`mod.auth.configure_node_state_action`](../../auth/types/mod.auth.configure_node_state_action.md).
The query is rejected before `identity` is resolved or the remote tree is
queried when the caller is not authorized, and a refused caller receives no
bytes.

The mount queries the remote node as the mounting node's own identity, not as
the caller and not as the user. The remote node answers under its own rules. A
node member of the remote node's swarm holds
[`mod.auth.see_node_state_action`](../../auth/types/mod.auth.see_node_state_action.md)
and reads the mounted tree. Writing through the mount answers to
[`mod.auth.configure_node_state_action`](../../auth/types/mod.auth.configure_node_state_action.md)
on the remote node, which no swarm membership grants: the remote node records a
node-local grant for the mounting node, or a signed contract carries it.

The operation queries the remote node before it records the mount point, with
`root` given and without it. A remote node that refuses the query, or does not
answer it, fails the operation and no mount is recorded.

## Arguments

* path (string8, required) – The local path at which to mount the remote subtree.
* identity (string8, required) – The identity of the remote node to mount from, given as a hex public key or a name resolved via the directory.
* root (string8) – The path on the remote node to use as the root of the mount. Defaults to `/` if omitted.

## Returned objects

The operation returns one of:
* An `error_message` object if there was an error.
* An `ack` object if the mount was established successfully.

## Examples

```shellsession
$ astral-query tree.mount_remote -path /remote/peer -identity somenode -root /mod -out json
{"Type":"ack","Object":null}
```
