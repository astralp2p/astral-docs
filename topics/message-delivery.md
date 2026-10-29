# Message Delivery

[`messaging.send_message`](../protocols/messaging/ops/messaging.send_message.md)
writes an outbox row, delivers a message to the recipient's node, and records
the result. The recipient's client need not be running.

```text
sender          sender's node        recipient's node       recipient
  | send              |                     |                   |
  |------------------>| write outbox        |                   |
  |                   | messaging.message   |                   |
  |                   |-------------------->| write inbox       |
  |                   |         ack         |                   |
  |       ID          |<--------------------|                   |
  |<------------------|                     |<----- read -------|
  |                   | messaging.receipt   |                   |
  |                   |<--------------------|                   |
  |                   | stamp FetchedAt     |                   |
  |                   |--------- ack ------>|                   |
```

## Delivery

`messaging.message` targets the recipient identity and carries one
[`messaging.message`](../protocols/messaging/types/messaging.message.md).
The query's caller supplies the sender; its target supplies the recipient.
The body carries neither identity.

The sending node routes on its own context with the sender as caller. Across a
link this produces a relay query preserving the caller's identity. A relay
contract locates the recipient's host; messaging publishes no separate mailbox
location record. Receipts use the same routing with the parties reversed.

A receiving node checks in this order:

1. **Path:** only `messaging.message` and `messaging.receipt` are handled.
   Other paths return `route_not_found` for other routers to try.
2. **Provenance:** only `network` origin or the node's marked internal send
   path is admitted. Other provenance, including local apps and MCP declared
   tools, is answered `origin not allowed: local` or `origin not allowed: mcp`
   before hosting is checked.
3. **Hosting:** an unhosted target returns `route_not_found`.
4. **Admission:** a receipt needs no action; a message requires
   [`receive_action`](../protocols/messaging/types/mod.messaging.receive_action.md).
   Denial answers the delivery with an `error_message` reading `not admitted`.

The node reads the one object a refused query carries before it answers the
refusal, because the sender writes it before reading the answer.

The receiving side relies on the sending node's send check. A query crossing a
link is indistinguishable there from a send; provenance is not an additional
cross-node send authorization check.

An accepted delivery reads one object within `delivery_timeout` and answers:

| Result | Condition |
| --- | --- |
| `ack` | Stored, or the same sender repeats an ID already in this inbox. |
| `not a message` | Wrong object type. |
| `the message names no id` | Zero ID. |
| `message too large` | Body exceeds `max_payload_bytes`. |
| `a message may not answer itself` | `ParentID` equals `ID`. |
| `the message answers one this node does not hold` | Recipient holds no parent in either box. |
| `a message is already stored under that id` | That inbox ID belongs to another sender. |
| `not a messaging participant` | Mailbox withdrawn after admission. |

Failures return `error_message`; storage failures carry the store's error.
A read timeout closes the delivery without an answer. Repeated delivery IDs
are stored once; this does not make separate `send_message` calls idempotent.
Nodes exchanging mail must share query names and positional wire layouts;
the message frame has no version marker, and fields are only appended.

## The sender's record

The sender's outbox and recipient's inbox are separately owned copies with
their own timestamps. The outbox records these facts:

| Stamp | Meaning |
| --- | --- |
| `CreatedAt` | Delivery attempted. |
| `LandedAt` | Recipient's node acknowledged storage. |
| `FailedAt` | Delivery is known to have failed. |
| `FetchedAt` | Recipient's node reported collection. |

An absent stamp means the fact is unknown. A missing acknowledgement can leave
an unstamped outbox even when the recipient stored the message. Validation and
send-authorization failures before delivery leave no outbox row.

The [send operation](../protocols/messaging/ops/messaging.send_message.md)
lists delivery errors and their effect on the outbox. `Err` contains bounded
refusal text, marked when cut; remote text is quoted data, not an instruction.
A refusal arrives on an accepted query, so it crosses relays unchanged. A node
that predates `not admitted` rejects with code 5 instead; across relays, when
none accepts the query, the first rejection other than generic code 1 is
preserved, so the sending node still reads code 5 as an admission refusal. See
[App Routing](app-routing.md#resolving-the-host).

## Receipts

An ordinary read of the owner's inbox marks the message read and reports
collection. Listing, waiting, peeking, and delegated reads report none.
Collection means the node processed the body for reading, not that a person
or model understood it; [read truncation](messaging.md#replies-and-read-bounds)
can omit the body after the stamps are written.

If the same node hosts the sender's mailbox, it stamps `FetchedAt` directly.
Otherwise it stamps `ReceiptDueAt`, sends one
[`messaging.receipt`](../protocols/messaging/types/messaging.receipt.md) to the
sender, and stamps `ReceiptStoredAt` after an `ack`. Only the first read that
sets `ReceiptDueAt` sends the receipt. Reading does not wait for it. Receipts
are not retried; a lost receipt can leave collection permanently unreported.

The sender's node matches an uncollected outbox row by message ID and recipient
(the receipt query's caller), stamps it, and answers `ack`. A missing,
mismatched, or already collected row returns `unknown message`; a wrong object
type returns `not a receipt`. Both are `error_message` objects. No receive
permission is required: the existing outbox row authorizes the receipt.
