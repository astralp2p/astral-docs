# user.remove_asset

Remove an object from the user's asset list. The caller must hold
`mod.user.admin_swarm_action`; rejected with code `4` otherwise. The change is
logged as a removal (tombstone) so other nodes pick it up via
`user.sync_assets`, and a `mod.user.notification` with event `assets` is pushed
to all linked siblings.

## Arguments

* id (object_id, required) – ID of the object to remove.

## Returned objects

The operation returns one of:
* An `ack` if the asset was removed.
* Rejected with the internal-error code if the database write failed.

## Examples

```shellsession
$ astral-query user.remove_asset -id id1.... -out text
#[ack]
```
