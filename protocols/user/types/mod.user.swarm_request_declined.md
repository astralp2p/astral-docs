# mod.user.swarm_request_declined

Emitted by user when the status of a request becomes `declined`. It travels as the `Data` of a [`mod.events.event`](../../events/types/mod.events.event.md) to the node's own receivers and never leaves the node.

A decline closes its request ([`mod.user.decline`](mod.user.decline.md)). A request that is `fulfilled` is never `declined`, so a decline that follows a signed contract emits nothing.

## Fields

* RequestID (object_id) – Entry ID of the declined request.

## Example

```json
{
  "Type": "mod.user.swarm_request_declined",
  "Object": {
    "RequestID": "data1eotsgeey6k7os9bhn5c6aow7rqf7jqmayqyq87bwpfatmo7e8mdcp"
  }
}
```
