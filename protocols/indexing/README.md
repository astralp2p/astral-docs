# indexing

The `indexing` protocol delivers repository change events to registered indexers. An indexer registers with `indexing.register_indexer` to receive a `nonce64` handle, then calls `indexing.subscribe` to receive a stream of `indexing.index` and `indexing.unindex` messages, acknowledging each with an `indexing.ack` before the next change is delivered.

Indexers persist their position per repository as a `Version` counter. The server tracks each indexer's confirmed state and retries unacknowledged changes with exponential back-off. `indexing.unregister_indexer` deletes an indexer's registration and its progress cursors; stored objects are unchanged.

`indexing.enable_repo` answers to
[`mod.auth.store_objects_action`](../auth/types/mod.auth.store_objects_action.md).
Indexing state is node-wide: enabling a repository indexes every object in it
from then on.

A registration belongs to the identity that registered it. An indexer name is
unique on the node: the owner registering the name again receives the same
nonce, and any other identity is refused. `indexing.register_indexer` and
`indexing.subscribe` require
[`mod.auth.serve_objects_action`](../auth/types/mod.auth.serve_objects_action.md)
for the `indexer` role, which the user identity holds by default.
`indexing.subscribe` serves the owner alone. `indexing.unregister_indexer`
serves the owner, and any other caller holding
[`mod.auth.admin_objects_action`](../auth/types/mod.auth.admin_objects_action.md).
A caller that the op does not serve for a registration receives the same
answer as for an unknown nonce. All three operations reject network-originated
queries.
