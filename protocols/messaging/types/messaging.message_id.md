# messaging.message_id

A 16-byte message identifier minted by the sender, rendered as 32 lowercase
hexadecimal characters. It names the same message in the sender's outbox and
recipient's inbox. The zero value names no message.

Returned by [`messaging.send_message`](../ops/messaging.send_message.md).

## Example

```json
"7f3a1c9e5b024d6810af2e7c94b5d3a6"
```
