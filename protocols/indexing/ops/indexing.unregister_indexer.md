# indexing.unregister_indexer

Unregister the indexer identified by `nonce`. The node deletes the indexer's registration and its per-repository progress cursors. Stored objects are unchanged. A later `indexing.register_indexer` with the same name starts a new registration with a new nonce and no progress.

## Arguments

* nonce (nonce64, required) – Nonce of the indexer to unregister.

## Returned objects

The operation returns one of:
* An `error_message` object if the nonce does not identify a known indexer or unregistration fails.
* An `ack` object on success.

## Examples

```shellsession
$ astral-query indexing.unregister_indexer -nonce 0102030405060708 -out json
{"Type":"ack","Object":{}}
```
