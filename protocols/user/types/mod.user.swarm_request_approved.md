# mod.user.swarm_request_approved

Emitted by user when the status of an expel request becomes `approved`. It travels as the `Data` of a [`mod.events.event`](../../events/types/mod.events.event.md) to the node's own receivers and never leaves the node.

An expel request is approved by a counting approval, or by the user key's [`mod.user.signed_expulsion`](mod.user.signed_expulsion.md) of the request's subject, which carries the request out. Only an expel request is approved: a contract request is answered with an offer and a join request by the carrier's signature, and neither emits this event. The user key's expel ceremony reacts to it ([`mod.user.approval`](mod.user.approval.md)).

## Fields

* RequestID (object_id) – Entry ID of the stored [`mod.user.signed_expel_request`](mod.user.signed_expel_request.md).
* ApprovalID (object_id) – The entry ID that approves the request: the lowest entry ID among the request's counting [`mod.user.signed_approval`](mod.user.signed_approval.md) entries, or, when none exists, the lowest entry ID among the user key's [`mod.user.signed_expulsion`](mod.user.signed_expulsion.md) entries whose `Subject` is the request's subject.

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
