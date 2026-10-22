# messaging.message_ref

A message in a selected mailbox, identified by box and ID. Used by
[`messaging.read_messages_request`](messaging.read_messages_request.md) and
its result's `NotFound` list. The box is required: a message to the same
identity has both an inbox and an outbox row.

## Fields

* Box (string8) – `inbox` or `outbox` in the selected mailbox, including for archived messages.
* ID ([messaging.message_id](messaging.message_id.md)) – Message identifier.

## Example

```json
{
  "Type": "messaging.message_ref",
  "Object": {
    "Box": "inbox",
    "ID": "7f3a1c9e5b024d6810af2e7c94b5d3a6"
  }
}
```
