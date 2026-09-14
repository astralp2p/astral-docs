# indexing.subscribe

Deliver pending index changes to a registered indexer identified by `nonce`. The op streams an `indexing.index` or `indexing.unindex` message for each pending change, waits for the caller to acknowledge each with an `indexing.ack`, then advances the indexer's stored state. When the indexer is caught up the op blocks until a new change arrives or the context is cancelled. Delivery is retried with exponential back-off (1 s initial, 1 min cap, factor 2) when the caller signals `ErrIndexingTemporarilyFailed`.

Network-originated queries are rejected. The caller must hold
[`mod.auth.serve_objects_action`](../../auth/types/mod.auth.serve_objects_action.md)
for the `indexer` role. The query is rejected when the caller is not
authorized. The node checks the permit when the subscription starts.

Only the owner of the registration subscribes to it, because each
acknowledgement advances the owner's stored state. Any other caller, including
a holder of
[`mod.auth.admin_objects_action`](../../auth/types/mod.auth.admin_objects_action.md),
receives the same `error_message` as for an unknown nonce.

## Arguments

* nonce (nonce64, required) – Nonce identifying the registered indexer.

## Returned objects

The operation returns one of:
* An `error_message` object `index not found` if the nonce does not identify a known indexer or the caller does not own the registration.
* An `error_message` object if a fatal error occurs.
* An `indexing.index` object when an object has been added to a repo.
* An `indexing.unindex` object when an object has been removed from a repo.

The caller must respond to each delivered change with an `indexing.ack`. The op returns an `error_message` if the ack's `Repo` or `Version` does not match the delivered change.

## Examples

```shellsession
$ astral-query indexing.subscribe -nonce 0102030405060708 -out json
{"Type":"indexing.index","Object":{"Repo":"myrepo","Version":1,"ObjectID":"<object-id>"}}
{"Type":"indexing.index","Object":{"Repo":"myrepo","Version":2,"ObjectID":"<object-id>"}}
```
