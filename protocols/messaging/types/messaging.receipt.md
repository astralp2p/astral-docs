# messaging.receipt

A collection report carried by a `messaging.receipt` query. Its caller is the
recipient and its target is the original sender. The sender's node stamps the
matching outbox row. [Receipts](../../../topics/message-delivery.md#receipts)
defines admission, acknowledgement, and retry behavior.

## Fields

* ID ([messaging.message_id](messaging.message_id.md)) – The identifier of the
  message that was collected, as the sender minted it.

## Example

```json
{
  "Type": "messaging.receipt",
  "Object": {
    "ID": "7f3a1c9e5b024d6810af2e7c94b5d3a6"
  }
}
```
