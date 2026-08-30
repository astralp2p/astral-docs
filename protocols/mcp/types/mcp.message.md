# mcp.message

One message an agent sends to another agent. Carried by the `mcp.message`
query, which the recipient's node answers by storing the message in the
recipient's inbox.

The message names neither party. The sender is the query's caller and the
recipient its target, both authenticated by the route, so a field naming either
would be a second claim about a fact the route already holds.

## Fields

* ID ([mcp.message_id](mcp.message_id.md)) – The message's identifier, minted
  by the sender. It names the message on both sides, and a delivery repeated
  under it is stored once.
* Content (string32) – The message body.
* Thread ([mcp.message_id](mcp.message_id.md)) – The exchange the message
  belongs to. A first message carries its own identifier. A reply copies the
  value it received, unchanged, so every message in one exchange carries the
  same label. The zero value names no thread, and the recipient's node stores
  the message under its own identifier instead.

## Example

```json
{
  "Type": "mcp.message",
  "Object": {
    "ID": "7f3a1c9e5b024d6810af2e7c94b5d3a6",
    "Content": "the index is rebuilt",
    "Thread": "0d41e6b28c5a4f9137be0a62d85c7f14"
  }
}
```
