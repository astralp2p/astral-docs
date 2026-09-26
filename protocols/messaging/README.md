# messaging

The `messaging` protocol carries mail between identities. A participant is an
[`Identity`](../../core-definitions/identity.md) with a mailbox: an inbox and an
outbox. A node hosts a participant's mailbox only under a hosting
[`Contract`](../../core-definitions/contract.md) the participant's identity
issues to that node — see [Hosting](#hosting). One node hosts the mailboxes of
many tenants and knows no relation between them. It knows no role a participant
plays either: an agent and an account owner are roles a product gives a
participant, and the node knows neither.

Three operations manage the identities whose mailboxes a node hosts.
`messaging.create_identity` mints a participant — a fresh identity, a signed
relay contract, a signed hosting contract, an optional
[`Alias`](../../core-definitions/alias.md), and an
[`apphost`](../apphost/README.md) access token the participant authenticates
with — and returns its token. `messaging.identity` reads one participant without
its token. `messaging.delete_identity` revokes the participant's tokens and
grants, unsets its alias, withdraws the node's hosting of its mailbox, and
deletes the mail it owns there.

Five operations are a participant's mail, and each acts on the caller's own
mailbox, which the node must host. `messaging.send_message` writes a
[`messaging.message`](types/messaging.message.md) to another participant,
`messaging.list_messages` lists a box without the bodies,
`messaging.read_messages` reads whole messages, each named by a
[`messaging.message_ref`](types/messaging.message_ref.md), `messaging.wait`
parks until a message arrives and answers what did, and `messaging.archive`
puts a message away. `messaging.list_messages` and `messaging.read_messages`
also read a mailbox this node hosts for another identity, when the authority
grants that reader
[`mod.messaging.read_mailbox_action`](types/mod.messaging.read_mailbox_action.md)
— see [Delegated read](#delegated-read).

Two queries carry mail between nodes, and neither is an operation.
`messaging.message` delivers a message to the recipient's identity, and
`messaging.receipt` tells the sender's identity that a body was handed out. A
node takes either only when it arrived over a link or came from the node's own
send path — see [Delivery](#delivery).

The [`mcp`](../mcp/README.md) endpoint serves the five mail operations to its
agents as tools, calling the messaging module directly, and `mcp.create_agent`
mints every agent as a participant, as `messaging.create_identity` does.

## Hosting

**A node hosts a mailbox only under a contract the mailbox's identity issues to
it.** The hosting contract is a
[`mod.auth.signed_contract`](../auth/types/mod.auth.signed_contract.md):

* Issuer – The mailbox identity.
* Subject – The hosting node.
* Permits – One permit for
  [`mod.messaging.host_mailbox_action`](types/mod.messaging.host_mailbox_action.md),
  with `Delegation` 0 and no constraints.
* ExpiresAt – The instant the node builds the contract plus the module's
  `hosting_duration`.

`messaging.create_identity` builds the contract, signs it with the keys the node
holds for both parties, indexes it with [`auth`](../auth/README.md), stores it,
and records it in the node's mailbox index. The node holds the mailbox
identity's key because it minted the identity, and the issuer is still the
mailbox identity.

**The mailbox identity is the root of the authority.** The module gives
[`auth`](../auth/README.md) one rule for `mod.messaging.host_mailbox_action`,
and the rule is not node-local: the action is granted when its `MailboxID` is
not the zero identity and its actor is `MailboxID` itself. A node asks the
action with itself as actor, so for any mailbox but its own it reaches the rule
only through a contract: `auth` walks the contracts the node is subject to and
asks the action again with each issuer as actor. No node hosts a mailbox for
itself: the hosting check refuses the node's own identity, and the zero
identity, before the index or `auth` is asked.

**A contract binds to its issuer's mailbox.** A contract the mailbox identity
issued to the node grants the node hosting of that one mailbox. A contract from
any other identity, the node's own contract to itself included, grants nothing:
its issuer is not `MailboxID`, and the rule grants the action to `MailboxID`
alone. A contract naming another node as subject grants this node nothing. A permit
carrying any constraint is refused.

**Relay and hosting are separate permits.** The identity's
[`mod.nodes.relay_for_action`](../nodes/types/mod.nodes.relay_for_action.md)
permit lets the node relay traffic on the identity's behalf, and the hosting
permit lets it hold the identity's mailbox. `messaging.create_identity` signs
them as two contracts. A relay permit alone never authorizes hosting, and a
hosting permit alone never authorizes relaying.

**Hosting and admission are separate checks.** A delivery from a sender to a
recipient is stored only when all of these pass:

1. The sending node hosts the sender's mailbox and grants
   [`mod.messaging.send_action`](types/mod.messaging.send_action.md), with the
   sender as actor, before the delivery leaves it. The recipient's node asks no
   send action: it takes a delivery only over a link or from its own send
   path, where this check ran — see [Delivery](#delivery).
2. The recipient's node hosts the recipient's mailbox.
3. The recipient's node grants
   [`mod.messaging.receive_action`](types/mod.messaging.receive_action.md), with
   the recipient as actor.

A hosting permit satisfies neither admission check, and an admission grant
establishes no hosting. Hosting gives no caller access to the mailbox: a mail
operation acts on the caller's own mailbox, and the route authenticates the
caller. Another identity reads the mailbox only under a separate grant,
[`mod.messaging.read_mailbox_action`](types/mod.messaging.read_mailbox_action.md),
and only reads it — see [Delegated read](#delegated-read).

**The mailbox index narrows routing and never authorizes.** A node keeps an
index of the hosting contracts it provisioned: one entry per mailbox identity,
naming the contract's [`Object ID`](../../core-definitions/object-id.md) and its
expiry. The index narrows which targets the module checks at all. A node hosts a
mailbox only while all of these hold:

* the index has an entry for the mailbox identity;
* the contract's expiry has not passed;
* `mod.messaging.host_mailbox_action` is granted with the node as actor and the
  mailbox identity as `MailboxID`.

The index cannot outlive the authority it records. An entry whose contract has
expired or no longer authorizes stays in the index and serves nothing.

**Each check happens when a request starts.** A delivery or a receipt is checked
when it arrives, before it is accepted. A mail operation other than
`messaging.read_messages` is checked before it is accepted, and the module
checks again when the operation calls it. `messaging.read_messages` learns the
mailbox it reads from its request, which arrives once the query is accepted, so
it is checked after the request arrives. A direct call to the module acting on a
mailbox is checked when it starts. No row is read or written before the check.
An operation that fails the check after it accepted the query answers
`not a messaging participant`, except a refused
[delegated read](#delegated-read), which ends the query with no answer. A
request that passed runs to its end: a `messaging.wait` parked before the
contract expired ends at its granted window.

**Expiry stops serving and deletes nothing.** A mailbox whose hosting contract
has expired receives no delivery and answers no mail operation, and its stored
mail stays. Losing hosting authority never authorizes destroying mail. No
operation renews a hosting contract.

**Only contracts this node provisioned are served.** The index names only the
hosting contracts this node signed when `messaging.create_identity` provisioned
a mailbox. A hosting contract indexed from elsewhere, through
[`auth.index`](../auth/ops/auth.index.md) or otherwise, grants
`mod.messaging.host_mailbox_action`, but the index has no entry for it, so the
node does not host that mailbox.

**Deletion is a local withdrawal and not a revocation.**
`messaging.delete_identity` removes the index entry and the mail the identity
owns on this node. The signed hosting contract stays valid until its expiry,
wherever a copy is held. This node stops hosting the mailbox because its index
no longer names it. A delivery or a send admitted before the withdrawal writes
its row before the withdrawal removes the mail, or writes nothing and answers
`not a messaging participant`.

## Boxes

**A participant has three boxes and two of them are one axis.** `inbox` is what
was written to it and `outbox` what it wrote; `archive` is neither, because it
is a state rather than a direction — a message put away is still one the
participant sent or received, and both listings exclude it. A message is in
exactly one of the first two for its whole life, and moves into and out of the
third.

`messaging.list_messages` names one of the three in `list`, and the narrowings
belong to the list named: an inbox narrows by who wrote and by what is unopened,
an outbox by who was written to and by what a recipient's node has stored and
not handed out. A narrowing that cannot apply to the named list is refused
rather than ignored, because ignoring it answers everything or nothing under a
question the caller thought it had asked.

**Only a read names a mailbox.** The owner of every row a mail operation writes
is the query's caller, authenticated by the route. `messaging.list_messages`
and `messaging.read_messages` read the caller's own mailbox unless they name
another, and another is read only as a [delegated read](#delegated-read), which
the authority grants and which changes nothing. No other value a caller passes
reaches another participant's mail.

## Authorization

A message between two participants crosses two permissions, and each belongs to
a different party. The `messaging` protocol holds neither: one node hosts the
mailboxes of many tenants and knows no relation between them, so it asks
[`auth`](../auth/README.md) and acts on the answer.

The sending node submits
[`mod.messaging.send_action`](types/mod.messaging.send_action.md), with the
sender as actor, before anything is written. The recipient's node submits
[`mod.messaging.receive_action`](types/mod.messaging.receive_action.md), with
the recipient as actor, before the delivery is accepted. A message is stored
only where both are granted, and only on a node that hosts the recipient's
mailbox: [Hosting](#hosting) lists the three checks, and
[Delivery](#delivery) gives the order in which the recipient's node makes its
own.

A send the sending side refuses is answered as one naming an identity the node
cannot resolve, `unknown recipient`, and no row is written. A participant cannot
tell a recipient it may not reach from one that is not there.

A delivery the receiving side refuses is rejected with `RejectNotAdmitted`,
reject code 5 — operation-specific, so above the generic codes
[`Query`](../../core-definitions/query.md) reserves. A sender whose node hosts
the recipient's mailbox reads `the recipient does not take messages from you`.
It is a separate answer from `route_not_found`, which the same node answers for
an identity whose mailbox it does not host and which a sender also reads when
the answering node could not be reached at all. The two are separate because
the sender acts on them differently: a sender turned away stops and asks
whoever owns it, and a sender that found nobody retries later.

**Across nodes a refusal reaches the sender as `route_not_found`.** The
recipient's node rejects the delivery with code 5 over the link as well. The
sending node reaches a recipient on another node through the recipient's relay
contract — see [Delivery](#delivery) — and its relay path takes a relay's
rejection as a failed relay: it tries the next relay, then answers
`route_not_found`. The sender reads `the recipient took nothing; they may not
exist, or their node may be unreachable`, and its outbox row is stamped failed
and carries no words. A sender tells a refusal from an absence only when the
recipient's mailbox is on the sender's own node.

**The code carries no reason.** [`auth`](../auth/README.md) answers one bit, so
a participant that admits nobody, an owner who does not admit this sender, and
an authority that would not decide all reach the sender as this one code.

**The code tells whoever receives it that the answering node hosts the
target's mailbox.** That is what separating the two answers costs, and the
receiving side pays it alone: a rejection is reachable only for an identity
whose mailbox the node hosts, so a sender on that node whose own side admits
every recipient learns which mailboxes the node hosts. A sending node that
routes a delivery to that node over a link receives the same code, although its
relay path does not pass the code on to the sender. The sending side's refusal stays
indistinguishable from a name that resolves to nobody.

**The node holds no reachability of its own.** A participant is reachable where
an `auth` handler, an active
[`Contract`](../../core-definitions/contract.md), or a configured external
authority says so, and a node with none of the three stores no message. What a
participant permits belongs to whoever owns it, and a node that held a copy
would hold a second answer to a question it does not decide.

A change of permission is answered on the next message the node asks about.
Nothing is in flight between two decisions: a message is a write that finishes
before its sender returns, so an owner narrowing what a participant may do has
nothing left to stop.

## Delivery

A message is a row in the recipient's inbox. `messaging.send_message` puts a
`messaging.message` query to the recipient's identity carrying one
[`messaging.message`](types/messaging.message.md); the recipient's node stores
it and answers an `ack`. The node answers, not the participant, so delivery
finishes inside the resolve deadline whether or not anything reading the
recipient's mail is running, and a recipient on another node is the same call
as one on the same node. Only a refusal by the receiving side reads differently
across nodes — see [Authorization](#authorization).

**The node routes a delivery as itself.** The query's caller is the sender and
its target the recipient, and the sending node routes it on its own context
rather than on one carrying the sender's identity. A link carries a query whose
caller is not the routing context's identity as a relay query naming the caller
and the target, so the recipient's node reads the sender as the caller. A
receipt is routed the same way with the parties reversed. The sending node
reaches a recipient on another node through a relay contract of the
recipient's that it holds; the protocol publishes no record of which node
hosts a mailbox.

**A node takes a delivery or a receipt in five steps**, in this order:

1. **Path.** A query addressed to any identity whose path is neither
   `messaging.message` nor `messaging.receipt` is answered `route_not_found`
   before anything else is asked. Hosting a mailbox claims no other query
   addressed to its identity: a mailbox is not a service, and the node's other
   routers try the query as if this module were absent.
2. **Provenance.** A `messaging.message` or `messaging.receipt` is taken only
   when it arrived over a [`Link`](../../core-definitions/link.md), carrying the
   `network` origin, or came from this node's own send path, which marks the
   queries it routes internally. Any other copy — one a local app routes itself,
   or one an [`mcp`](../mcp/README.md) declared tool puts for an agent with the
   `mcp` origin — is rejected with the generic reject code 1, whatever its
   target and before the hosting check. The recipient's side asks no send
   action, so a copy that skipped the sending node's check is refused here; a
   copy addressed to a mailbox on another node would cross a link, where the far
   node cannot tell it from a send.
3. **Hosting.** A target whose mailbox this node does not host, as
   [Hosting](#hosting) defines it, is answered `route_not_found`, and the
   node's other routers try it.
4. **Receipt.** A `messaging.receipt` is accepted without asking
   [`auth`](../auth/README.md) — see [the sender's record](#the-senders-record).
5. **Admission.** A `messaging.message` asks
   [`mod.messaging.receive_action`](types/mod.messaging.receive_action.md), with
   the target as actor and the caller as `FromID`. A refusal is rejected with
   `RejectNotAdmitted`, reject code 5, and a grant accepts the delivery.

An accepted delivery reads one object within the module's `delivery_timeout`
and answers it with one of:

* An `ack` once the message is stored, or when the same sender repeats a
  delivery of an identifier this inbox already holds from it.
* An `error_message` object reading `not a message` if the object is not a
  `messaging.message`.
* An `error_message` object reading `the message names no id` for the zero
  identifier, `message too large` for a body over the module's
  `max_payload_bytes`, `a message may not answer itself` for a `ParentID` equal
  to its `ID`, or `the message answers one this node does not hold` for a
  parent the recipient holds in neither box.
* An `error_message` object reading `a message is already stored under that id`
  when another sender's message already holds that identifier in this inbox.
* An `error_message` object reading `not a messaging participant` when the
  mailbox was withdrawn after the delivery was accepted, or carrying the store's
  own words when the row cannot be written.

A delivery whose object is not read within `delivery_timeout` is closed with no
answer.

The row is a [`messaging.stored_message`](types/messaging.stored_message.md):
the sender, the recipient, the body, the message it answers, the instant the
node wrote it, the instant it was read and the instant it was put away. The
sender is the query's caller and the recipient its target. Neither is a field of
the [`messaging.message`](types/messaging.message.md) that carried it, so a
sender claims neither — the frame that crosses the link and the record the node
keeps are two types, and only the second names a party.

The stored instant is a claim about the node and not about the recipient, who
may not run for days. It is named for what the node did, beside a sender's row
whose own instants are named the same way.

## Replies

**A reply names the message it answers, and an exchange is a query.** A
[`messaging.message`](types/messaging.message.md) carries the identifier of the
one message it answers, and a message answering none carries the zero value. An
exchange is the chain those links make. Nothing is opened, owned, closed or
expired, and no node holds a record that another node must agree with.

**The link is a claim about another message, never about a party.** It is the
sender's, as the body is, while the sender and the recipient are the route's.
Naming a message means naming a 128-bit identifier that was never published, and
every row carries the identity of whoever wrote it.

**A reply names a message both parties hold.** The sending participant's node
refuses a parent that participant does not hold, and the recipient's node
refuses one the recipient does not hold. A message has one of each, so a parent
is a message between exactly these two parties, and no participant replies into
an exchange it is not part of. A message put away still counts as held:
archiving does not unsee it.

**That makes an exchange a forest.** Every parent names a message stored
earlier, so no chain of links returns to where it began and a reader walking one
needs no record of where it has been. A message naming itself is refused as the
cheapest case of the same rule.

**Nodes that exchange mail carry the same names.** A node answers a delivery and
a receipt only under the query names and object types it carries, and the frame
is positional with no version marker. Nodes carrying different messaging names
do not deliver to each other, so nodes that exchange mail move together.

**Replies are read, never followed.** `messaging.read_messages` answers a
message with the messages that name it, one level. Walking further is the
reader's to do, and the node holds no depth it must agree with anyone about.

## Reading

**Nothing is claimed.** `messaging.wait` parks until the caller's inbox holds a
message it has not put away, and answers what it found without touching a row.
Two readers waiting at once are answered the same messages, and neither takes
anything from the other. A reader that stops between the answer and the work
leaves the mailbox exactly as it was.

**A park names the window it was given.** `messaging.wait` takes the window the
caller asks for in `timeout`, grants it up to the module's `wait_max`, and
answers `Granted` beside `Waited` — the budget and the spend. An ask over the
ceiling is clamped rather than refused: a refusal would make the deployment's
ceiling part of every client's configuration, where a clamp is read off the
answer. A caller naming no window is granted the module's `wait_default`.
`TimedOut` says the granted window closed with nothing new.

**The inbox has a cursor and the node does not hold it.** Every envelope carries
its `Cursor`, and a caller passing the greatest one it has seen back as `since`
sees only what was written after. `messaging.wait` answers that value as
`NextSince`, and an answer with nothing newer repeats the cursor it was given,
so following it costs the caller no memory. The cursor is a position in the
order the node wrote the rows, never an instant: a row's stored time is chosen
before the row commits, so a cursor over time steps past a message that had not
appeared yet, and does so permanently. The other two lists are histories read
newest first and refuse a cursor rather than answer one wrongly.

**Reading is a separate act, and it is not a claim.** `messaging.read_messages`
opens what it is given and stamps each inbox message read. A second read answers
the same messages unchanged, so a caller that retries a call whose answer it
never saw loses nothing. A read of another identity's mailbox stamps nothing at
all — see [Delegated read](#delegated-read).

**A read answers the shape of an exchange and carries part of it.** Every
message a read names carries the identifier of each of its direct replies in
`ChildIDs`, whatever else the answer carries: a reader that cannot see a reply
exists cannot ask for it, and a count names no message. How much of those
replies comes back beside it is the caller's — none, envelopes, or the bodies
too. A reply's body is opt-in because handing one out stamps it read and tells
its sender it was collected, which a reader asking about the parent never asked
for.

**An answer is bounded, and says where the bound fell.** A read names at most
twenty messages and carries at most ten replies of each, and the bodies one
answer carries are bounded by the module's `max_read_bytes`. The message the
caller named is charged against that budget before its replies, so an overflow
drops what was not asked for first, and a message whose body was left out for
room is marked `Truncated`. The read stamp and the collection report are made
as each row is read, before its body is charged, so a message left out for room
is stamped read and reported collected all the same. An identifier the
participant does not hold is reported rather than refused: one wrong identifier
does not cost the rest of the batch.

**Archiving is what says the participant is done.** `messaging.archive` stamps
the message put away, and a message put away is excluded from both listings and
never answered by `messaging.wait` again. It is the participant's own
bookkeeping: it names no other node, crosses no link, and the other party learns
nothing from it. It is also the one stamp with an inverse — `undo` puts the
message back, through the same operation.

The answer is `Changed` rather than `Archived`, because under `undo` the second
would name the opposite of what happened: what the call reports is whether it
was the one that moved the message. It is false alike for a message already
where the caller asked and for one the caller does not hold, which the
participant acts on the same way — and separating them would say whether an
identifier it does not hold exists.

**A delivery that arrives twice is stored once.** The
[`messaging.message_id`](types/messaging.message_id.md) is minted by the sender
and keys the row, so a sender that repeats a delivery after a lost `ack` leaves
one message.

A hosted mailbox answers `messaging.message` and `messaging.receipt`, and no
other query: [Delivery](#delivery) gives the order in which a node checks the
path, the provenance, the hosting and the admission of each.

## The sender's record

A send is a row in the sender's outbox, written before the delivery is
attempted and stamped by what the delivery returns. The two rows have different
owners: the recipient's row is the recipient's, and across nodes it is not on
the sender's machine at all, while what a sender knows survives whether or not
the recipient's node is reachable.

The row is a [`messaging.stored_message`](types/messaging.stored_message.md) in
the outbox, carrying the recipient, the body, and four instants — when the send
was attempted, when the recipient's node acknowledged the write, when the
delivery was known to have failed, and when the body was handed out. Each names
when a fact became true, and an unset instant is the absence of that fact rather
than a value somebody chose. A row nothing has stamped is a send whose fate is
unknown, which is the honest answer after a crash: an acknowledgement that
never arrived proves nothing about the write.

A send refused before delivery is attempted leaves no row: an unresolvable
recipient, `mod.messaging.send_action` denied, a body over the bound, or a
parent the sending participant does not hold. A stored list of refusals would
tell a recipient that refuses apart from one that does not exist, which is the
collapse the refusal is built on.

`messaging.list_messages` answers the rows of one mailbox, whichever list it
names: the caller's own, or one the caller reads as a
[delegated read](#delegated-read). A row the receiving side rejected
carries the refusal when the recipient's mailbox is on the sender's own node;
across nodes the rejection arrives as `route_not_found`, and the row carries no
words — see [Authorization](#authorization). A row a recipient's node refused
after accepting the delivery carries that node's own words, which are quoted
material and never a field to act on. The words are bounded where they are
stored and marked where they were cut: a refusing node decides neither how much
of the reader's context they occupy nor whether the reader can tell it read the
whole of them.

**A collection is reported by the recipient's node.** When the body is handed
out and the same node hosts the sender's mailbox, that node stamps the sender's
row directly. Otherwise the recipient's node stamps its own row `ReceiptDueAt`,
puts a `messaging.receipt` query to the sender's identity carrying one
[`messaging.receipt`](types/messaging.receipt.md), and stamps `ReceiptStoredAt`
once the sender's node stamps the row and answers an `ack`. Only the read that
first stamps `ReceiptDueAt` sends a receipt, and only a read of the recipient's
own mailbox stamps it: a [delegated read](#delegated-read) hands bodies out and
reports no collection.

The stamp reports that the body was handed out and never that anyone considered
it, and neither `messaging.wait` nor `messaging.list_messages` hands a body out
— a recipient learns a message exists without its sender learning anything. A
recipient that reads its mail and stops marks every message it opened
collected.

**A receipt is one attempt.** The fact it carries is already true and durable on
the node that sends it, so a receipt lost in transit leaves the sender believing
a message was never collected — wrong, permanently, and in the direction that
waits rather than the one that assumes. Nothing retries one, and the recipient's
read never waits on one.

**The outbox row is the receipt's permission.** The sender's node admits a
`messaging.receipt` without asking [`auth`](../auth/README.md): the row is the
consequence of a permitted past act, and the receipt says one thing about that
one message. Directions are granted per side and the two are independent, so
asking `mod.messaging.receive_action` here would refuse a receipt wherever the
sender's inbound direction is narrower than its outbound one — the ordinary
case, not the edge one. A node that does not host the target's mailbox answers
`route_not_found`. An accepted receipt is answered an `ack` when it stamps the
target's outbox row for that identifier, sent to the caller and not yet
stamped collected. Any other receipt is answered an `error_message` object
reading `unknown message` — a row already stamped included — and an object
that is not a `messaging.receipt` is answered `not a receipt`.

## Delegated read

**Another identity reads a mailbox where the authority grants it, and only reads
it.** `messaging.list_messages` takes a `mailbox` argument, and a
[`messaging.read_messages_request`](types/messaging.read_messages_request.md)
carries a `Mailbox` field. Absent, or naming the caller, either reads the
caller's own mailbox as the rest of this document describes. Naming another
identity makes the call a delegated read: the caller lists or reads that
mailbox's rows and changes none of them. Only these two operations take a
mailbox. `messaging.send_message`, `messaging.archive` and `messaging.wait` act
on the caller's own mailbox alone, and the [`mcp`](../mcp/README.md) endpoint's
tools name no mailbox.

**The node asks, and the authority decides.** A delegated read is answered only
when these pass, in this order, before any row is read:

1. The caller is neither the zero identity nor this node's own identity. The
   caller need not have a mailbox on this node.
2. This node hosts the named mailbox, as [Hosting](#hosting) defines it. A
   mailbox this node does not serve is refused.
3. [`mod.messaging.read_mailbox_action`](types/mod.messaging.read_mailbox_action.md)
   is granted with the caller as actor and the named mailbox as `MailboxID`.

A refused delegated read reads nothing, and its caller receives no bytes.
`messaging.list_messages` rejects the query at every step.
`messaging.read_messages` rejects the query at step 1, before it accepts it. It
learns the mailbox from its request, which arrives once the query is accepted,
so a refusal at step 2 or step 3 ends the query with no answer.

A `mailbox` argument of `messaging.list_messages` that resolves to no identity
is rejected before step 1, and its caller receives no bytes. A `from` or `to`
that resolves to no identity differs: it is answered `unknown correspondent`.

No credential is borrowed. The reader authenticates as itself, and the mailbox's
own token is neither presented nor needed. The node holds no rule about who
reads whose mailbox: it asks [`auth`](../auth/README.md) on every delegated read
and acts on the answer, so a changed answer applies to the next read.

**The module gives [`auth`](../auth/README.md) no rule for the action.** Being
the mailbox identity grants nothing. An `auth` handler registered for
`mod.messaging.read_mailbox_action` or the external authority configured for it
grants the action, and the node acts on their answer as it does for
[Authorization](#authorization). A node with neither refuses every delegated
read.

**The action refuses every permit.** A
[`mod.auth.permit`](../auth/types/mod.auth.permit.md) for
`mod.messaging.read_mailbox_action` is refused whether or not it carries a
constraint. No permit carries a delegated read, so no
[`mod.auth.signed_contract`](../auth/types/mod.auth.signed_contract.md) carries
one: in a contract whose subject is the reader, a permit for the action grants
nothing, whoever the issuer is, and `auth` asks the handlers and the external
authority about the reader itself. The refusal covers contracts carrying this
action and no other. A contract carrying
[`mod.auth.sudo_action`](../auth/types/mod.auth.sudo_action.md) lets its subject
act as its issuer, and a read the subject makes as the issuer is the issuer's
read.

**A delegated read never stamps.** It stamps no `ReadAt` or `ReceiptDueAt` on
the mailbox's inbox rows, sends no `messaging.receipt`, and stamps no
`FetchedAt` on a sender's outbox row on this node. This holds for the messages
the read names and for their replies under `Children` `full` alike. The
mailbox's owner finds its mailbox as it left it: an unread message stays unread,
and no sender learns of a collection its recipient did not make. Everything else
about a read holds: the bounds, `ChildIDs`, the replies answered beside a
message, and `Truncated`.

## Origin

Every operation rejects a query carrying the `network` origin, which a query
arriving over a [`Link`](../../core-definitions/link.md) carries, and a query
carrying the `mcp` origin, which a query a declared tool of the
[`mcp`](../mcp/README.md) endpoint puts for an agent carries. The
refusal comes before any action is submitted and before the caller is checked,
and a refused caller receives no bytes. A query that omits a required argument,
or carries an argument that does not parse as its type, is rejected with the
generic reject code 1 before the operation runs, and so before the origin
refusal.

**The mail operations answer only a caller whose mailbox this node hosts.** On
the caller's own mailbox, `messaging.send_message`, `messaging.list_messages`,
`messaging.wait` and `messaging.archive` reject a caller that is the zero
identity or whose mailbox this node does not host, as [Hosting](#hosting)
defines it, before anything is read or written. `messaging.read_messages`
rejects the zero identity and the node's own identity before it accepts the
query. `messaging.read_messages` learns the mailbox it reads from its request,
which arrives once the query is accepted, and answers a caller whose own
mailbox this node does not host `not a messaging participant` before any row is
read. The node hosts no mailbox for its own identity, so a local caller that
carries no identity and acts as the node reaches no mailbox. A
[delegated read](#delegated-read) is checked differently: its caller need not
have a mailbox here, the mailbox it names must, and the node's own identity is
refused as a reader.

`messaging.create_identity` and `messaging.delete_identity` require
[`mod.auth.admin_manage_apps_action`](../auth/types/mod.auth.admin_manage_apps_action.md),
and `messaging.identity` requires
[`mod.auth.see_node_state_action`](../auth/types/mod.auth.see_node_state_action.md).
A participant holds neither by default.

`messaging.message` and `messaging.receipt` are not operations and take no
operation's refusal — each is addressed to a participant's identity rather than
to a node's, and a caller reaches both over a link. A node puts the deliveries
and receipts it sends with no origin and with its send path's internal mark:
their path is fixed and addressed to a participant, and no operation answers
either name. A node takes either only when it arrived over a link or carries
that mark. A copy with any other provenance — no origin, the `local` origin or
the `mcp` origin — is rejected with the generic reject code 1, whatever its
target, before the hosting check. A copy that passes is checked for hosting as
[Delivery](#delivery) orders it.

**A participant reaches its own mail through apphost.** A participant's access
token is an [`apphost`](../apphost/README.md) access token, and apphost's
endpoints stamp no origin, so the token's bearer reaches the mail operations
there — and through them the participant's own mailbox, and another mailbox
only to read it, where the authority grants the bearer
[`mod.messaging.read_mailbox_action`](types/mod.messaging.read_mailbox_action.md).

**An MCP tool carries no query.** The [`mcp`](../mcp/README.md) endpoint's mail
tools call the messaging module directly as the authenticated agent, so no
origin applies to them, and the module's hosting check does: a tool reaches a
mailbox only where the matching operation would. Where the operation refuses a
caller whose mailbox this node does not host, the tool answers
`not a messaging participant`. No tool names a mailbox: an agent's tools act on
the agent's own mailbox alone.

## Configuration

The module reads `messaging.yaml`. Every key is optional, and a key left out
takes its default:

```yaml
hosting_duration: 87600h
token_duration: 8760h
delivery_timeout: 15s
wait_default: 2m
wait_max: 15m
max_payload_bytes: 65536
max_read_bytes: 65536
```

* `hosting_duration` – The lifetime of the hosting contract
  `messaging.create_identity` signs, counted from the instant it builds the
  contract. Defaults to 87600 hours — ten 365-day years, the lifetime of the
  relay contract `messaging.create_identity` signs beside it, which no key
  changes.
* `token_duration` – The lifetime of the access token
  `messaging.create_identity` issues when the caller names no `duration`.
  Defaults to 8760 hours, 365 days.
* `delivery_timeout` – Bounds one delivery and one receipt on the sending node,
  and the read of either on the answering node. Defaults to 15 seconds.
* `wait_default` – The window `messaging.wait` grants a caller naming none.
  Defaults to 2 minutes.
* `wait_max` – The most any `messaging.wait` is granted, `wait_default`
  included. Defaults to 15 minutes.
* `max_payload_bytes` – The longest body, in bytes, a send accepts and a
  delivery stores. Defaults to 65536.
* `max_read_bytes` – The most body bytes one `messaging.read_messages` answer
  carries. Defaults to 65536.

**The deployment names both wait bounds.** What caps a held call is the
client's own request timeout and any proxy in front of it, which the node cannot
know.
