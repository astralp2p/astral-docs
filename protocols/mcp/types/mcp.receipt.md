# mcp.receipt

The recipient's node telling a sender that a message's body was handed out.
Carried by the `mcp.receipt` query, which the sender's node answers by stamping
the message collected in that sender's outbox.

The receipt names neither party. The recipient is the query's caller and the
original sender its target — the reverse of an
[`mcp.message`](mcp.message.md) — both authenticated by the route, so a field
naming either would be a second claim about a fact the route already holds.

A receipt reports that the recipient's node handed the body out, and never that
the recipient's model considered it. A node asserts what it did; it never speaks
for a model.

The receipt carries one attempt and no state of its own. The fact it reports is
already true and durable on the node that sends it, so a receipt lost in transit
costs the sender a stamp and nothing else. Nothing retries one.

## Fields

* ID ([mcp.message_id](mcp.message_id.md)) – The identifier of the message that
  was collected, as the sender minted it.

## Example

```json
{
  "Type": "mcp.receipt",
  "Object": {
    "ID": "7f3a1c9e5b024d6810af2e7c94b5d3a6"
  }
}
```
