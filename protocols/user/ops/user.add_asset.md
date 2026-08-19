# user.add_asset

Add an object to the user's asset list. The caller must hold
`mod.user.admin_swarm_action`; rejected with code `4` otherwise. The change is
recorded in this node's asset log and a `mod.user.notification` with event
`assets` is pushed to all linked siblings so they can pull the update.

## Arguments

* id (object_id, required) – ID of the object to add.

## Returned objects

The operation returns one of:
* An `ack` if the asset was added.
* Rejected with the internal-error code if the database write failed.

## Examples

```shellsession
$ astral-query user.add_asset -id id1.... -out text
#[ack]
```
