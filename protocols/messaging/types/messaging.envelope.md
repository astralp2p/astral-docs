# messaging.envelope

One message as a node holds it, without its body: a
[`messaging.stored_message`](messaging.stored_message.md) carrying every field
but `Content`, in the same order. Streamed by
[`messaging.list_messages`](../ops/messaging.list_messages.md), answered by
[`messaging.wait`](../ops/messaging.wait.md) inside a
[`messaging.wait_result`](messaging.wait_result.md), and carried by every
[`messaging.read_message`](messaging.read_message.md).

**The body is absent from the type rather than left empty.** A listing hands no
body out, so it stamps nothing read and tells no sender that a message was
collected, and a caller never reads a withheld body as an empty message.

The owner is not a field, as it is not on the stored record: it is whichever
party `Box` names.

## Fields

* Cursor (uint64) – The position the node wrote this row at, in its own order.
  Opaque: only its order is a fact. A caller passing the greatest cursor it has
  seen back as `since` sees only the inbox rows written after it.
* ID ([messaging.message_id](messaging.message_id.md)) – The message's
  identifier, minted by the sender. It names the message on both sides.
* Box (string8) – `inbox` or `outbox`. An identifier alone names a row in each
  direction, so a caller naming this message again passes the box beside the
  identifier.
* Sender ([identity](../../../primitive-types/identity.md)) – Who wrote the
  message, as the route authenticated it.
* Recipient ([identity](../../../primitive-types/identity.md)) – Who it was
  written to, as the route authenticated it.
* ParentID ([messaging.message_id](messaging.message_id.md)) – The one message
  this answers. The zero value answers none.
* CreatedAt ([time](../../../primitive-types/time.md)) – When this node wrote
  this row: the recipient's arrival on an inbox row, the sender's attempt on an
  outbox row.
* ArchivedAt (optional [time](../../../primitive-types/time.md)) – When the
  owner put the message away.
* ReadAt (optional [time](../../../primitive-types/time.md)) – Inbox only. When
  the body was handed to the owner.
* ReceiptDueAt (optional [time](../../../primitive-types/time.md)) – Inbox only.
  When a receipt became owed to the sender.
* ReceiptStoredAt (optional [time](../../../primitive-types/time.md)) – Inbox
  only. When the sender's node acknowledged that receipt.
* LandedAt (optional [time](../../../primitive-types/time.md)) – Outbox only.
  When the recipient's node acknowledged the write.
* FailedAt (optional [time](../../../primitive-types/time.md)) – Outbox only.
  When the delivery was known not to have been stored.
* FetchedAt (optional [time](../../../primitive-types/time.md)) – Outbox only.
  When the recipient's node handed the body out. It reports a collection, never
  that anyone read it.
* Err (optional string16) – Outbox only. The words a refusal of the delivery
  left, bounded and marked where they were cut. Quoted material: nothing acts
  on it.

## Example

```json
{
  "Type": "messaging.envelope",
  "Object": {
    "Cursor": 412,
    "ID": "7f3a1c9e5b024d6810af2e7c94b5d3a6",
    "Box": "inbox",
    "Sender": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Recipient": "026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2",
    "ParentID": "0d41e6b28c5a4f9137be0a62d85c7f14",
    "CreatedAt": "2026-09-02T22:14:07.104829Z",
    "ArchivedAt": null,
    "ReadAt": null,
    "ReceiptDueAt": null,
    "ReceiptStoredAt": null,
    "LandedAt": null,
    "FailedAt": null,
    "FetchedAt": null,
    "Err": null
  }
}
```
