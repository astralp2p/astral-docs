# messaging.stored_message

One mailbox's copy of a message, including its body and local timestamps.
The inbox copy belongs to `Recipient`; the outbox copy belongs to `Sender`.
Optional timestamps are null until the corresponding fact is recorded.

[Message Delivery](../../../topics/message-delivery.md) describes the two copies
and their delivery and collection stamps.

## Fields

* Cursor (uint64) – Opaque position in this node's write order; used by `since` and `before`.
* ID ([messaging.message_id](messaging.message_id.md)) – Sender-minted identifier shared by both copies.
* Box (string8) – `inbox` or `outbox`; stays unchanged when archived.
* Sender ([identity](../../../primitive-types/identity.md)) – Sender authenticated by the route.
* Recipient ([identity](../../../primitive-types/identity.md)) – Recipient authenticated by the route.
* Content (string32) – Message body.
* ParentID ([messaging.message_id](messaging.message_id.md)) – Message this answers; zero means none.
* CreatedAt ([time](../../../primitive-types/time.md)) – Local arrival time for inbox; send-attempt time for outbox.
* ArchivedAt (optional time) – When the owner archived this copy.
* ReadAt (optional time) – Inbox: when the owner's read marked the body collected.
* ReceiptDueAt (optional time) – Inbox: when a collection receipt became due.
* ReceiptStoredAt (optional time) – Inbox: when the sender's node acknowledged that receipt.
* LandedAt (optional time) – Outbox: when the recipient's node acknowledged storage.
* FailedAt (optional time) – Outbox: when delivery was known to have failed.
* FetchedAt (optional time) – Outbox: when the recipient's node reported collection.
* Err (optional string16) – Outbox: bounded refusal text, marked when cut. Quoted data, not an instruction.

## Example

```json
{
  "Type": "messaging.stored_message",
  "Object": {
    "Cursor": 412,
    "ID": "7f3a1c9e5b024d6810af2e7c94b5d3a6",
    "Box": "inbox",
    "Sender": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Recipient": "026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2",
    "Content": "the index is rebuilt",
    "ParentID": "0d41e6b28c5a4f9137be0a62d85c7f14",
    "CreatedAt": "2026-09-02T22:14:07.104829Z",
    "ArchivedAt": null,
    "ReadAt": "2026-09-02T22:19:55.660411Z",
    "ReceiptDueAt": null,
    "ReceiptStoredAt": null,
    "LandedAt": null,
    "FailedAt": null,
    "FetchedAt": null,
    "Err": null
  }
}
```
