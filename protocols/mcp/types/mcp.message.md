# mcp.message

One message an agent sends to another agent. Carried by the `mcp.message`
query, which the recipient's node answers by storing the message in the
recipient's inbox.

A field is otherwise only ever appended. The frame is positional and carries no
version marker, so a slot that changes meaning is read as the field that used to
be there, without an error to notice it — which is what retiring Thread did, and
why that retirement is an incompatible change rather than a tidy-up.

The message names neither party. The sender is the query's caller and the
recipient its target, both authenticated by the route, so a field naming either
would be a second claim about a fact the route already holds.

## Fields

* ID ([mcp.message_id](mcp.message_id.md)) – The message's identifier, minted
  by the sender. It names the message on both sides, and a delivery repeated
  under it is stored once.
* Content (string32) – The message body.
* ParentID ([mcp.message_id](mcp.message_id.md)) – The one message this message
  answers. The zero value answers none. A parent the recipient's node does not
  hold is stored as it stands; the one link refused is a message naming itself.

## Example

```json
{
  "Type": "mcp.message",
  "Object": {
    "ID": "7f3a1c9e5b024d6810af2e7c94b5d3a6",
    "Content": "the index is rebuilt",
    "ParentID": "0d41e6b28c5a4f9137be0a62d85c7f14"
  }
}
```
