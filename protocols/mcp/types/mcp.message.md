# mcp.message

One message an agent sends to another agent. Carried by the `mcp.message`
query, which the recipient's node answers by storing the message in the
recipient's inbox.

A field is only ever appended. The frame is positional and carries no version
marker, so a slot that changed meaning would be read as the field that used to
be there, without an error to notice it.

The message names neither party. The sender is the query's caller and the
recipient its target, both authenticated by the route, so a field naming either
would be a second claim about a fact the route already holds.

## Fields

* ID ([mcp.message_id](mcp.message_id.md)) – The message's identifier, minted
  by the sender. It names the message on both sides, and a delivery repeated
  under it is stored once.
* Content (string32) – The message body.
* Thread ([mcp.message_id](mcp.message_id.md)) – Dead. It named a flat exchange
  label before a reply named its parent. Carried for compatibility alone: no
  node reads it, a sender may set it, a recipient ignores it, and the slot is
  never reused — a value here and a value in ParentID are the same sixteen
  bytes, and nothing in the frame tells them apart.
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
    "Thread": "00000000000000000000000000000000",
    "ParentID": "0d41e6b28c5a4f9137be0a62d85c7f14"
  }
}
```
