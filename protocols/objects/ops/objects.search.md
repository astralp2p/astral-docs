# objects.search

Run a search query across registered searchers. The query string follows the `objects.search_query` grammar (bare words, `tag:value`, `-tag:value`, `?tag:value`, `~tag:value`).

The caller must hold
[`mod.auth.see_objects_action`](../../auth/types/mod.auth.see_objects_action.md).
The operation answers an `error_message` reading `not permitted` before any
repository is opened when the caller is not authorized.

Other nodes are reached two ways, both only within the `network` zone:

* The swarm searcher is a registered searcher. It asks every other member of
  the swarm, concurrently.
* `sources` names nodes the caller chooses. `sources_only` decides whether they
  are asked on top of the registered searchers or alone.

The node asks other nodes as itself. It authorized its caller; the other node
trusts that decision. A source equal to this node is skipped.

A query arriving from the network runs without the `network` zone: the node
answers from its own searchers and asks no other node.

## Arguments

* q (string, required) – The search query.
* repo (string8) – If set, only matches whose objects exist in this repository are returned.
* zone (zone) – Limits the query's routing zone and never widens it. Without it, the routing zone stands.
* sources (string) – Comma-separated identities or aliases to ask. A repeated entry is asked once. Absent by default.
* sources_only (bool) – `true` asks only `sources` and runs no registered searcher. Defaults to `false`, which asks `sources` on top of the registered searchers.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object if the repository is not found, a `sources` entry does not resolve to an identity, or the search fails to start.
* A stream of `mod.objects.search_result` objects (deduplicated by object id) followed by an `eos` object. The search context has a one-minute timeout.

## Examples

```shellsession
$ astral-query objects.search -q 'mime:text/plain hello' -out json
{"Type":"mod.objects.search_result","Object":{"SourceID":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f","ObjectID":"data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}}
{"Type":"eos","Object":null}
```
