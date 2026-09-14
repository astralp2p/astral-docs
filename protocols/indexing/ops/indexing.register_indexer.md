# indexing.register_indexer

Register a new indexer with a human-readable name for the caller and return its assigned nonce. The nonce is used in subsequent `indexing.subscribe` and `indexing.unregister_indexer` calls. Network-originated queries are rejected.

The caller must hold
[`mod.auth.serve_objects_action`](../../auth/types/mod.auth.serve_objects_action.md)
for the `indexer` role. The query is rejected when the caller is not
authorized.

The registration belongs to the caller. A name is unique on the node. When the caller already owns a registration with the name, the op returns that registration's nonce. When another identity owns it, the op returns an error and no nonce.

## Arguments

* name (string, required) – Human-readable name for the indexer.

## Returned objects

The operation returns one of:
* An `error_message` object `indexer name registered by another identity` if another identity owns a registration with the name.
* An `error_message` object if registration fails.
* A `nonce64` object containing the assigned indexer nonce.

## Examples

```shellsession
$ astral-query indexing.register_indexer -name myindexer -out json
{"Type":"nonce64","Object":"0102030405060708"}
```
