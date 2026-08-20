# user.sync_with

Trigger this node to pull the user's asset list from another node by calling
`user.sync_assets` against it and applying every entry it returns to this
node's own list. Used to force a one-shot reconciliation without waiting for a
sibling notification.

The caller must hold `mod.user.admin_swarm_action`; rejected with code `4`
otherwise. The op changes what this node carries, as `user.add_asset` and
`user.remove_asset` do — the node named in the call decides the entries this
node ends up holding, so it is the same authority rather than a read.

## Arguments

* node (identity, required) – Identity of the node to sync with, normally a
  sibling. The node is not required to be one: the caller names where the
  entries come from.
* start (uint64, optional) – Height to start syncing from. Defaults to `0`.

## Returned objects

The operation returns one of:
* An `ack` once the sync completes.
* An `error_message` if the remote sync failed.

## Examples

```shellsession
$ astral-query user.sync_with -node 0282fee8...779b2c -out text
#[ack]
```
