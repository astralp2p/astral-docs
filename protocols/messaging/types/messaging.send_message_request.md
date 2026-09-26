# messaging.send_message_request

What a participant asks
[`messaging.send_message`](../ops/messaging.send_message.md) to send: the
recipient, the body, and the message it answers. Read from the operation's
input stream.

The sender is not a field. It is the query's caller, so no value here sends as
anyone else.

## Fields

* To (string8) – The recipient, given as a hex public key or a name resolved via
  the directory.
* Content (string32) – The message body, at most the module's
  `max_payload_bytes` long.
* ParentID ([messaging.message_id](messaging.message_id.md)) – The one message
  this message answers. The zero value answers none. A nonzero value names a
  message the sender holds, in either box and whether or not it was put away.

## Example

```json
{
  "Type": "messaging.send_message_request",
  "Object": {
    "To": "scout",
    "Content": "the index is rebuilt",
    "ParentID": "0d41e6b28c5a4f9137be0a62d85c7f14"
  }
}
```
