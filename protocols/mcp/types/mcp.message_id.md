# mcp.message_id

The identifier of one [`mcp.message`](mcp.message.md). Sixteen bytes, minted by
the sender, rendered as thirty-two lowercase hexadecimal characters wherever it
is read as text.

The identifier is the message's name on both sides: the recipient reads by it,
and the recipient's node keys the stored row on it, so a delivery that arrives
twice is stored once. The zero identifier names no message.

**The width is sixteen bytes because an inbox keeps a message.** The identifier
competes against every message a node has stored rather than against the ones
in flight, so a 64-bit identifier reaches a one-in-a-million collision at six
million messages — a count a node outlives.

## Example

```json
"7f3a1c9e5b024d6810af2e7c94b5d3a6"
```
