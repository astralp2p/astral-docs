# mod.user.swarm_request_expired

Emitted by user when the status of a request becomes `expired`. It travels as the `Data` of a [`mod.events.event`](../../events/types/mod.events.event.md) to the node's own receivers and never leaves the node.

The request's Timeout has passed and the request is neither `fulfilled`, `declined` nor `approved`.

## Fields

* RequestID (object_id) – Entry ID of the expired request.

## Example

```json
{
  "Type": "mod.user.swarm_request_expired",
  "Object": {
    "RequestID": "data1eotsgeey6k7os9bhn5c6aow7rqf7jqmayqyq87bwpfatmo7e8mdcp"
  }
}
```
