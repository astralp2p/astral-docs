# indexing

The `indexing` protocol delivers repository change events to registered indexers. An indexer registers with `indexing.register_indexer` to receive a `nonce64` handle, then calls `indexing.subscribe` to receive a stream of `indexing.index` and `indexing.unindex` messages, acknowledging each with an `indexing.ack` before the next change is delivered.

Indexers persist their position per repository as a `Version` counter. The server tracks each indexer's confirmed state and retries unacknowledged changes with exponential back-off. `indexing.unregister_indexer` deletes an indexer's registration and its progress cursors; stored objects are unchanged.

`indexing.enable_repo` and `indexing.subscribe` answer to
[`mod.auth.store_objects_action`](../auth/types/mod.auth.store_objects_action.md).
Indexing state is node-wide: enabling a repository indexes every object in it
from then on, and a subscription consumes an indexer's change stream and
advances its cursor. `indexing.register_indexer` and
`indexing.unregister_indexer` submit no action.
