# user.remove_asset

Remove an object from the user's asset list. The caller must hold
`mod.user.admin_swarm_action`; answered `not permitted` otherwise. The change is
logged as a removal (tombstone) so other nodes pick it up via
`user.sync_assets`, and a `mod.user.notification` with event `assets` is pushed
to all linked siblings.

## Arguments

* id (object_id, required) – ID of the object to remove.

The `id` is an [`Object ID`](../../../core-definitions/object-id.md) with a
nonzero `Size`. The operation answers an `Object ID` whose `Size` is 0 with an
`error_message` reading `partial object id` and writes nothing. The node logs
no error for that refusal.

An asset is recorded under an `Object ID` with a nonzero `Size`, because
[`user.add_asset`](user.add_asset.md) refuses any other. No asset is reachable
by a [`Partial Object ID`](../../../core-definitions/object-id.md), so a
removal given one logs a tombstone matching no asset and replicates it to every
linked sibling.

The `Object ID` of the `Empty Object` has a `Size` of 0, so this operation
refuses it too.

## Returned objects

The operation returns one of:
* An `ack` if the asset was removed.
* An `error_message` reading `partial object id` if `id` is a `Partial Object ID`.
* An `error_message` if the database write failed.

## Examples

```shellsession
$ astral-query user.remove_asset -id id1.... -out text
#[ack]
```
