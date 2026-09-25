# messaging.message_ref

One row of the caller's mailbox, named by box and identifier. Named in a
[`messaging.read_messages_request`](messaging.read_messages_request.md) and
answered in a [`messaging.read_messages_result`](messaging.read_messages_result.md)
for a row the caller does not hold.

**The box is not optional and never inferred.** An identifier alone names a row
in each direction — a participant writing to itself holds both — and the
archive spans both directions, so a reference names the box an envelope
reported beside the identifier.

The owner is not a field. It is the caller of the operation the reference is
passed to, so no reference reaches another participant's mail.

## Fields

* Box (string8) – `inbox` or `outbox`: which of the caller's rows. An archived
  message is named by the box it sits in.
* ID ([messaging.message_id](messaging.message_id.md)) – The message's
  identifier.

## Example

```json
{
  "Type": "messaging.message_ref",
  "Object": {
    "Box": "inbox",
    "ID": "7f3a1c9e5b024d6810af2e7c94b5d3a6"
  }
}
```
