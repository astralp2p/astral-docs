# nodes.migrate_session

Migrate an existing session onto a different link. Used to move traffic between links, e.g. to switch networks or shed pressure.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The query is rejected before the session or the link is looked up when the
caller is not authorized, and a refused caller receives no bytes.

## Arguments

* session_id (nonce64, required) – The id of the session to migrate.
* link_id (nonce64, required) – The id of the destination link.
* start (bool) – If true, drive the migration locally without expecting a signalling handshake (manual mode). Otherwise the operation negotiates the migration via `mod.nodes.migrate_signal` exchanges over the channel.
* out (string) – Output format hint for the channel (e.g. `json`).

## Returned objects

The operation returns one of:
* An `error_message` object if the session or link cannot be found, the session is in an invalid state, or the session is already on the target link.
* An `ack` object when `start=true` and the manual migration completes successfully.
* A sequence of `mod.nodes.migrate_signal` objects (`switched`, then `done`) interleaved with peer signals (`ready`, `resume`) when running the negotiated handshake.

## Examples

```shellsession
$ astral-query nodes.migrate_session -session_id a1b2c3d4e5f60718 -link_id 7c1a93b50f2e4d18 -start true -out json
{"Type":"ack","Object":null}
```
