# user.remove_asset

Remove an object from the user's asset list. The caller must hold
`mod.user.admin_swarm_action`; rejected with code `4` otherwise. The change is
logged as a removal (tombstone) so other nodes pick it up via
`user.sync_assets`, and a `mod.user.notification` with event `assets` is pushed
to all linked siblings.

## Arguments

* id (object_id, required) – ID of the object to remove.

The `id` is an [`Object ID`](../../../core-definitions/object-id.md) with a
nonzero `Size`. The operation rejects an `Object ID` whose `Size` is 0 with
code `2` and writes nothing. The node logs no error for that rejection.

An asset is recorded under an `Object ID` with a nonzero `Size`, because
[`user.add_asset`](user.add_asset.md) refuses any other. No asset is reachable
by a [`Partial Object ID`](../../../core-definitions/object-id.md), so a
removal given one logs a tombstone matching no asset and replicates it to every
linked sibling.

The `Object ID` of the `Empty Object` has a `Size` of 0, so this operation
rejects it too.

## Returned objects

The operation returns one of:
* An `ack` if the asset was removed.
* Rejected with code `2` if `id` is a `Partial Object ID`.
* Rejected with the internal-error code if the database write failed.

## Examples

```shellsession
$ astral-query user.remove_asset -id id1.... -out text
#[ack]
```
