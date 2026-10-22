# messaging.message

The body carried by a `messaging.message` delivery query. The query's caller
is the sender and its target is the recipient. The receiving node stores a
[`messaging.stored_message`](messaging.stored_message.md).

[Message Delivery](../../../topics/message-delivery.md#delivery) defines
admission, replies, and the positional wire layout.

## Fields

* ID ([messaging.message_id](messaging.message_id.md)) – Nonzero sender-minted identifier; repeated deliveries from that sender are stored once.
* Content (string32) – Message body, bounded by `max_payload_bytes`.
* ParentID ([messaging.message_id](messaging.message_id.md)) – Message this answers; zero means none. Both parties must hold the parent in either box, archived or not; it cannot equal `ID`.

## Example

```json
{
  "Type": "messaging.message",
  "Object": {
    "ID": "7f3a1c9e5b024d6810af2e7c94b5d3a6",
    "Content": "the index is rebuilt",
    "ParentID": "0d41e6b28c5a4f9137be0a62d85c7f14"
  }
}
```
