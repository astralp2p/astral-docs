# messaging.receipt

The recipient's node telling a sender that a message's body was handed out.
Carried by the `messaging.receipt` query, which the sender's node answers by
stamping the message collected in that sender's outbox.

The receipt names neither party. The recipient is the query's caller and the
original sender its target — the reverse of a
[`messaging.message`](messaging.message.md) — both authenticated by the route,
so a field naming either would be a second claim about a fact the route already
holds.

A receipt reports that the recipient's node handed the body out, and never that
anyone considered it. A node asserts what it did; it never speaks for whatever
reads the mail.

The receipt carries one attempt and no state of its own. The fact it reports is
already true and durable on the node that sends it, so a receipt lost in transit
costs the sender a stamp and nothing else. Nothing retries one.

A receipt is sent only when the node that handed the body out does not host
the sender's mailbox; a node that hosts it stamps the sender's row directly.
The sender's node takes a receipt only over a link or from its own send path,
and admits it by the matching outbox row, asking
[`auth`](../../auth/README.md) nothing: see [Delivery](../README.md#delivery)
and [the sender's record](../README.md#the-senders-record). A receipt naming no
such row, or one already stamped collected, is answered `unknown message`.

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
