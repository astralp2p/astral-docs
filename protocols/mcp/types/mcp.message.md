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

## Example

```json
{
  "Type": "mcp.message",
  "Object": {
    "ID": "7f3a1c9e5b024d6810af2e7c94b5d3a6",
    "Content": "the index is rebuilt"
  }
}
```
