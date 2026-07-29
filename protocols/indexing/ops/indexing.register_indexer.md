# indexing.register_indexer

Register a new indexer with a human-readable name and return its assigned nonce. The nonce is used in subsequent `indexing.subscribe` and `indexing.remove_index` calls.

## Arguments

* name (string, required) – Human-readable name for the indexer.

## Returned objects

The operation returns one of:
* An `error_message` object if registration fails.
* A `nonce64` object containing the assigned indexer nonce.

## Examples

```shellsession
$ astral-query indexing.register_indexer -name myindexer -out json
{"Type":"nonce64","Object":"0102030405060708"}
```
