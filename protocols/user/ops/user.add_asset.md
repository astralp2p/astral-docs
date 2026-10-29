# user.add_asset

Add an object to the user's asset list. The caller must hold
`mod.user.admin_swarm_action`; answered `not permitted` otherwise. The change is
recorded in this node's asset log and a `mod.user.notification` with event
`assets` is pushed to all linked siblings so they can pull the update.

## Arguments

* id (object_id, required) – ID of the object to add.

The `id` is an [`Object ID`](../../../core-definitions/object-id.md) with a
nonzero `Size`. The operation answers an `Object ID` whose `Size` is 0 with an
`error_message` reading `partial object id` and writes nothing. The node logs
no error for that refusal.

An asset is recorded under the `Object ID` it was added under, and that record
replicates to every linked sibling.
[`objects.purge`](../../objects/ops/objects.purge.md) matches an asset by an
`Object ID` with a nonzero `Size`, so an asset recorded under a
[`Partial Object ID`](../../../core-definitions/object-id.md) matches no such
test, and the object it names is purged on this node and on each sibling that
received the record.

The `Object ID` of the `Empty Object` has a `Size` of 0, so this operation
refuses it too.

## Returned objects

The operation returns one of:
* An `ack` if the asset was added.
* An `error_message` reading `partial object id` if `id` is a `Partial Object ID`.
* An `error_message` if the database write failed.

## Examples

```shellsession
$ astral-query user.add_asset -id id1.... -out text
#[ack]
```
