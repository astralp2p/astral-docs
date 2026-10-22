# Mailbox Hosting

A node hosts a [`messaging`](../protocols/messaging/README.md) mailbox under a
contract from the mailbox identity. Hosting, relaying, sending, receiving, and
reading another mailbox are separate permissions.

## Hosting

[`messaging.create_mailbox`](../protocols/messaging/ops/messaging.create_mailbox.md)
mints an identity, an optional alias, an apphost access token, and two signed
contracts. Both contracts have the mailbox identity as issuer and this node as
subject. Each lasts ten 365-day years and has one unconstrained permit with
`Delegation` 0:

* [`mod.nodes.relay_for_action`](../protocols/nodes/types/mod.nodes.relay_for_action.md)
  permits traffic on the identity's behalf.
* [`mod.messaging.host_mailbox_action`](../protocols/messaging/types/mod.messaging.host_mailbox_action.md)
  permits hosting its mailbox.

The node holds the new identity's key and signs for both parties. The identity
is a mailbox participant, not a node user; it never receives the node's claim
contract. Neither contract grants permission to send or receive mail.

The node indexes and stores the contracts, then records the hosting contract's
object ID and expiry in its mailbox index. Hosting requires all three:

1. The mailbox index contains the identity.
2. The indexed hosting contract has not expired.
3. The node is authorized for `host_mailbox_action` with that `MailboxID`.

The zero identity and the node's own identity cannot have hosted mailboxes.
The action's root rule grants it to `MailboxID` itself; contract authorization
lets the hosting node reach that rule through the mailbox issuer. A contract
from another identity grants no authority over this mailbox. Constrained
hosting permits are refused. Indexing a contract through `auth.index` alone
does not provision a mailbox.

## Expiry and deletion

Hosting contracts have no renewal operation or configurable lifetime. Expiry
stops new requests but deletes neither the index entry nor stored mail.
Deliveries and receipts then receive `route_not_found`; mail operations refuse
the owner. An admitted delivery, receipt, or wait runs to its normal end.

[`messaging.delete_mailbox`](../protocols/messaging/ops/messaging.delete_mailbox.md)
revokes tokens, withdraws local grants, unsets the alias, then removes the
mailbox index entry and owned mail together. Correspondents' copies remain.
Signed relay and hosting contracts remain valid until expiry; deletion withdraws
this node's indexed mailbox rather than revoking those contracts.

A failure before the final write keeps the index entry for retry. If that write
fails, the entry and mail remain, but the mailbox stays unserved until a retry
removes it or a restart serves it again; tokens are already revoked. A send or
delivery admitted before withdrawal either writes before deletion or fails
with `not a messaging participant` and writes nothing.

## Authorization

The sending node asks
[`mod.messaging.send_action`](../protocols/messaging/types/mod.messaging.send_action.md)
with the sender as actor. The receiving node asks
[`mod.messaging.receive_action`](../protocols/messaging/types/mod.messaging.receive_action.md)
with the recipient as actor. Both must be granted. The node defines no tenant
relationships; `auth` handlers, contracts, or an external authority decide.
With no grant, no message is sent or admitted. Nonempty permit constraints are
refused for both actions. Permission changes apply to subsequent checks.

A denied send returns `unknown recipient: <to>` and writes no outbox row. A
denied receive rejects with `RejectNotAdmitted` (code 5); the sender reads
`the recipient does not take messages from you`. This rejection reveals that
the answering node hosts the mailbox, but carries no reason for the denial.
An unhosted target returns `route_not_found`. [Message Delivery](message-delivery.md)
describes how those results reach the sender.

## Delegated read

`messaging.list_messages` accepts `mailbox`; `messaging.read_messages_request`
accepts `Mailbox`. An omitted value or the caller's identity selects its own
mailbox. Another identity selects a delegated read, checked in this order:

1. The caller is neither the zero identity nor this node's identity.
2. This node hosts the named mailbox.
3. [`mod.messaging.read_mailbox_action`](../protocols/messaging/types/mod.messaging.read_mailbox_action.md)
   is granted with the caller as actor and the selected `MailboxID`.

The reader authenticates as itself and needs no mailbox here. The action has
no built-in grant and refuses every permit, including unconstrained permits.
Only an `auth` handler or external authority grants it directly to the reader.
This restriction does not prevent `sudo_action` from allowing an identity to
act as another identity.

A delegated read changes no `ReadAt`, `ReceiptDueAt`, or `FetchedAt`, sends no
receipt, and follows the usual read bounds. It permits no sending, waiting, or
archiving. MCP mail tools expose no delegated read.

A denied listing rejects the query. A read learns `Mailbox` from its input
after accepting the query; denied hosting or read authority then closes the
query without an answer. Neither path returns bytes or reads rows on denial.

## Origin and admission

All messaging operations reject `network` and `mcp` origins before checking the
caller or submitting an action. Missing required arguments and malformed
argument types are rejected earlier with generic reject code 1.

Own-mailbox operations require a hosted caller. Listing, sending, waiting, and
archiving check hosting before accepting the query and again on entering the
module. `read_messages` rejects the zero and node identities before accepting;
after reading its request it checks hosting and returns
`not a messaging participant` for an unhosted own mailbox. Hosting checks
precede all mailbox reads and writes.

Creation and deletion require `admin_manage_apps_action`; `messaging.mailbox`
requires `see_node_state_action`. A participant holds neither by default.

Apphost endpoints authenticate the mailbox's token and stamp no origin, so
participants use the mail operations there. MCP mail tools call the module
directly: no query origin applies, but hosting and mail permissions still do.
An unhosted caller receives `not a messaging participant`.

The `messaging.message` and `messaging.receipt` delivery queries target mailbox
identities, not node operations. Their [admission rules](message-delivery.md#delivery)
allow links and the node's internal send path.
