# user.sync_assets

Stream this node's asset log starting from a given height, then the next
height the caller should ask for. Used by sibling nodes to keep their copies
of the user's asset list in sync.

Each entry is a `mod.user.op_update` carrying the nonce, the object ID, and
whether the entry is a removal (tombstone).

The caller must hold `mod.user.see_swarm_action`; sibling nodes sync as the
user, who holds it by default. Rejected with code `2` if the database read
failed, and with code `4` if the caller is not authorized.

## Arguments

* start (uint64, optional) – Lowest log height to include (inclusive). Defaults
  to `0` (full log).

## Returned objects

The operation streams:
* Zero or more `mod.user.op_update` objects in ascending height order.
* A final `uint64` — the next height the caller should pass as `start` on the
  next call. When there were no rows it equals `start`; otherwise it is one
  past the highest height streamed.

## Examples

```shellsession
$ astral-query user.sync_assets -start 0 -out json
{"Type":"mod.user.op_update","Object":{"Nonce":"...","ObjectID":"id1...","Removed":false}}
{"Type":"mod.user.op_update","Object":{"Nonce":"...","ObjectID":"id2...","Removed":true}}
{"Type":"uint64","Object":2}
```
