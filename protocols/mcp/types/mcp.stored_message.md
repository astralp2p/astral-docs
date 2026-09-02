# mcp.stored_message

One message as a node holds it, in one agent's box. Every message a node carries
is two of these — the sender's and the recipient's, differing in `Box` and in
their owner and in nothing else — and across nodes only one of them is on any
given machine.

**This and [`mcp.message`](mcp.message.md) are two types because they answer two
questions.** `mcp.message` is the frame that crosses a link, and it names
neither party because the route already does. This is the record a node holds
once the delivery lands: the parties the route authenticated, the box the row
sits in, and the instants that node stamped. Neither is derivable from the
other. One type carrying both would either put a spoofable claim on the wire or
leave a reader unable to say who wrote what —
[`mcp.agent_info`](mcp.agent_info.md) sits beside [`mcp.agent`](mcp.agent.md)
for the same reason.

**An unset instant is the absence of the fact.** It is never a value somebody
chose, and never a zero one. A row carrying `CreatedAt` alone is a send whose
fate is unknown, which is the honest answer after a crash: an acknowledgement
that never arrived proves nothing about the write.

**The owner is not a field.** It is whichever party the box names — the
recipient on an inbox row, the sender on an outbox row — so a record that stated
it could state it wrong.

## Fields

* Cursor (uint64) – The position the node wrote this row at, in its own order.
  Opaque: only its order is a fact. Only the inbox pages by it; the other two
  lists are histories read newest first.
* ID ([mcp.message_id](mcp.message_id.md)) – The message's identifier, minted by
  the sender. It names the message on both sides.
* Box (string8) – `inbox` or `outbox`. A message is in one of them for its whole
  life. The archive is a state rather than a third box, and `ArchivedAt` carries
  it.
* Sender ([identity](../../../primitive-types/identity.md)) – Who wrote the
  message, as the route authenticated it.
* Recipient ([identity](../../../primitive-types/identity.md)) – Who it was
  written to, as the route authenticated it.
* Content (string32) – The message body.
* ParentID ([mcp.message_id](mcp.message_id.md)) – The one message this answers.
  The zero value answers none.
* CreatedAt ([time](../../../primitive-types/time.md)) – When this node wrote
  this row: the recipient's arrival on an inbox row, the sender's attempt on an
  outbox row.
* ArchivedAt (optional [time](../../../primitive-types/time.md)) – When the
  owner put the message away. The owner's own bookkeeping; it crosses no link,
  and it is the one stamp with an inverse.
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
  that a model read it.
* Err (optional string16) – Outbox only. The recipient's node's own words for a
  refusal, bounded by the storing node and marked where it was cut. Quoted
  material: another operator wrote it, and nothing acts on it.

## Example

```json
{
  "Type": "mcp.stored_message",
  "Object": {
    "Cursor": 412,
    "ID": "7f3a1c9e5b024d6810af2e7c94b5d3a6",
    "Box": "inbox",
    "Sender": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Recipient": "026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2",
    "Content": "the index is rebuilt",
    "ParentID": "0d41e6b28c5a4f9137be0a62d85c7f14",
    "CreatedAt": "2026-09-02T22:14:07.104829Z",
    "ReadAt": "2026-09-02T22:19:55.660411Z"
  }
}
```
