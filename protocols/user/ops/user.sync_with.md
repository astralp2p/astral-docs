# user.sync_with

Trigger this node to pull the user's asset list from another node by calling
`user.sync_assets` against it and applying every entry it returns to this
node's own list. Used to force a one-shot reconciliation without waiting for a
sibling notification.

`user.sync_with` passes `start` to `user.sync_assets` as the next height this
node recorded after its last completed sync with that node, or `0` when no
sync with that node has completed. This node records the returned next height
when the sync completes.

The caller must hold `mod.user.admin_swarm_action`. Rejected with code `3` if
`identity` does not resolve or resolves to the anonymous identity, and with code
`4` if the caller is not authorized. `identity` is resolved before the caller is
authorized. The op changes what this node carries, as `user.add_asset` and
`user.remove_asset` do — the node named in the call decides the entries this
node ends up holding, so it is the same authority rather than a read.

## Arguments

* identity (string8, required) – Identity of the node to sync with, normally a
  sibling, given as a hex public key or a name resolved via the directory. The
  node is not required to be a sibling: the caller names where the entries come
  from.

## Returned objects

The operation returns one of:
* An `ack` once the sync completes.
* An `error_message` if the remote sync failed.

## Examples

```shellsession
$ astral-query user.sync_with -identity 0282fee8...779b2c -out text
#[ack]
```
