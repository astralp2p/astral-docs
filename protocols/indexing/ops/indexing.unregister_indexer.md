# indexing.unregister_indexer

Unregister the indexer identified by `nonce`. The node deletes the indexer's registration and its per-repository progress cursors. Stored objects are unchanged. A later `indexing.register_indexer` with the same name starts a new registration with a new nonce and no progress. Network-originated queries are rejected.

The owner of the registration unregisters it without a permit. Any other caller must hold
[`mod.auth.admin_objects_action`](../../auth/types/mod.auth.admin_objects_action.md).
A caller that is neither receives the same `error_message` as for an unknown nonce.

## Arguments

* nonce (nonce64, required) – Nonce of the indexer to unregister.

## Returned objects

The operation returns one of:
* An `error_message` object `index not found` if the nonce does not identify a known indexer, or the caller neither owns the registration nor holds `mod.auth.admin_objects_action`.
* An `error_message` object if unregistration fails.
* An `ack` object on success.

## Examples

```shellsession
$ astral-query indexing.unregister_indexer -nonce 0102030405060708 -out json
{"Type":"ack","Object":{}}
```
