# mod.user.swarm_request_filed

Emitted by user when a valid request first appears in the node's SwarmState. It travels as the `Data` of a [`mod.events.event`](../../events/types/mod.events.event.md) to the node's own receivers and never leaves the node.

Every event of the swarm is a signal to read the entries again: a receiver reads the current state before it acts, and copes with a duplicate. The node emits it for every valid entry it holds, and a receiver keeps those whose `Subject` it serves. The node emits nothing at startup for entries it already holds.

A request is valid once the merge check stores it ([SwarmState entries](../README.md#swarmstate-entries)).

## Fields

* RequestID (object_id) – Entry ID of the stored signed request.
* Kind (string8) – Object type of the signed request: `mod.user.signed_contract_request`, `mod.user.signed_join_request` or `mod.user.signed_expel_request`.

## Example

```json
{
  "Type": "mod.user.swarm_request_filed",
  "Object": {
    "RequestID": "data1eotsgeey6k7os9bhn5c6aow7rqf7jqmayqyq87bwpfatmo7e8mdcp",
    "Kind": "mod.user.signed_contract_request"
  }
}
```
