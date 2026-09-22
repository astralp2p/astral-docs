# user.add_asset

Add an object to the user's asset list. The caller must hold
`mod.user.admin_swarm_action`; rejected with code `4` otherwise. The change is
recorded in this node's asset log and a `mod.user.notification` with event
`assets` is pushed to all linked siblings so they can pull the update.

## Arguments

* id (object_id, required) – ID of the object to add.

The `id` is an [`Object ID`](../../../core-definitions/object-id.md) with a
nonzero `Size`. The operation rejects an `Object ID` whose `Size` is 0 with
code `2` and writes nothing. The node logs no error for that rejection.

An asset is recorded under the `Object ID` it was added under, and that record
replicates to every linked sibling.
[`objects.purge`](../../objects/ops/objects.purge.md) matches an asset by an
`Object ID` with a nonzero `Size`, so an asset recorded under a
[`Partial Object ID`](../../../core-definitions/object-id.md) matches no such
test, and the object it names is purged on this node and on each sibling that
received the record.

The `Object ID` of the `Empty Object` has a `Size` of 0, so this operation
rejects it too.

## Returned objects

The operation returns one of:
* An `ack` if the asset was added.
* Rejected with code `2` if `id` is a `Partial Object ID`.
* Rejected with the internal-error code if the database write failed.

## Examples

```shellsession
$ astral-query user.add_asset -id id1.... -out text
#[ack]
```
