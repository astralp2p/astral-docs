# mod.user.swarm_request_approved

Emitted by user when the status of an expel request becomes `approved`. It travels as the `Data` of a [`mod.events.event`](../../events/types/mod.events.event.md) to the node's own receivers and never leaves the node.

Only an expel request is approved: a contract request is answered with an offer and a join request by the carrier's signature, and neither emits this event. The user key's expel ceremony reacts to it ([`mod.user.approval`](mod.user.approval.md)).

## Fields

* RequestID (object_id) – Entry ID of the stored [`mod.user.signed_expel_request`](mod.user.signed_expel_request.md).
* ApprovalID (object_id) – The lowest entry ID among the request's counting [`mod.user.signed_approval`](mod.user.signed_approval.md) entries.

## Example

```json
{
  "Type": "mod.user.swarm_request_approved",
  "Object": {
    "RequestID": "data1eotsgeey6k7os9bhn5c6aow7rqf7jqmayqyq87bwpfatmo7e8mdcp",
    "ApprovalID": "data1q9m3fd0d3x5kz7vu4tn2yjh8lcw6ar5p0se4gbxn8o2ty7k1hvnqe"
  }
}
```
