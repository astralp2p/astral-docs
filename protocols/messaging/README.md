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
its token. `messaging.delete_identity` withdraws the node's hosting of one
mailbox and deletes the mail it owns there.

Five operations are a participant's mail, and each acts on the caller's own
mailbox, which the node must host. `messaging.send_message` writes a
[`messaging.message`](types/messaging.message.md) to another participant,
`messaging.list_messages` lists a box without the bodies,
`messaging.read_messages` reads whole messages by
[`messaging.message_id`](types/messaging.message_id.md), `messaging.wait` parks
until a message arrives and answers what did, and `messaging.archive` puts a
message away.

Two queries carry mail between nodes, and neither is an operation.
`messaging.message` delivers a message to the recipient's identity, and
`messaging.receipt` tells the sender's identity that a body was handed out.

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
* ExpiresAt – The instant of signing plus the module's `hosting_duration`.

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
asks the action again with each issuer as actor. The mailbox index never names
the node's own identity, so no node hosts a mailbox for itself.

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
recipient is stored only when three checks pass, in this order:

1. The recipient's node hosts the recipient's mailbox.
2. The sending side granted
   [`mod.messaging.send_action`](types/mod.messaging.send_action.md), with the
   sender as actor, before the delivery left the sender's node.
3. The recipient's node grants
   [`mod.messaging.receive_action`](types/mod.messaging.receive_action.md), with
   the recipient as actor.

A hosting permit satisfies neither admission check, and an admission grant
establishes no hosting. The sender's node sends only for a sender whose mailbox
it hosts. Hosting gives no caller access to the mailbox: a mail operation acts
on the caller's own mailbox, and the route authenticates the caller.

**The mailbox index narrows routing and never authorizes.** A node keeps an
index of the hosting contracts it provisioned: one entry per mailbox identity,
naming the contract's [`Object ID`](../../core-definitions/object-id.md) and its
expiry. The index narrows which targets the module checks at all. A node hosts a
mailbox only while all of these hold:

* the index has an entry for the mailbox identity, and the entry names a
  contract;
* the contract's expiry has not passed;
* `mod.messaging.host_mailbox_action` is granted with the node as actor and the
  mailbox identity as `MailboxID`.

The index cannot outlive the authority it records. An entry whose contract has
expired or no longer authorizes stays in the index and serves nothing.

**Each check happens when a request starts.** A delivery or a receipt is checked
when it arrives, before it is accepted. A mail operation, and a direct call to
the module acting on a mailbox, is checked when it starts, before anything is
read or written. A request that passed runs to its end: a `messaging.wait`
parked before the contract expired ends at its granted window.

**Expiry stops serving and deletes nothing.** A mailbox whose hosting contract
has expired receives no delivery and answers no mail operation, and its stored
mail stays. Losing hosting authority never authorizes destroying mail. No
operation renews a hosting contract.

**Only contracts this node provisioned are served.** The index names only the
hosting contracts this node signed when it provisioned a mailbox, as
`messaging.create_identity` does. A hosting contract indexed from elsewhere,
through [`auth.index`](../auth/ops/auth.index.md) or otherwise, grants
`mod.messaging.host_mailbox_action`, but the index has no entry for it, so the
node does not host that mailbox.

**Deletion is a local withdrawal and not a revocation.**
`messaging.delete_identity` removes the index entry and the mail the identity
owns on this node. The signed hosting contract stays valid until its expiry,
wherever a copy is held. This node stops hosting the mailbox because its index
no longer names it.

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

**No operation names an owner.** The owner of every row a mail operation reads
or writes is the query's caller, authenticated by the route. No argument names
an owner, so no value a caller passes reaches another participant's mail.

## Authorization

A message between two participants crosses two permissions, and each belongs to
a different party. The `messaging` protocol holds neither: one node hosts the
mailboxes of many tenants and knows no relation between them, so it asks
[`auth`](../auth/README.md) and acts on the answer.

The sender submits
[`mod.messaging.send_action`](types/mod.messaging.send_action.md) before
anything is written. The recipient's node submits
[`mod.messaging.receive_action`](types/mod.messaging.receive_action.md), with
the recipient as actor, before the delivery is accepted. A message is stored
only where both are granted, and only on a node that hosts the recipient's
mailbox: [Hosting](#hosting) gives the order of the three checks.

A send the sending side refuses is answered as one naming an identity the node
cannot resolve, `unknown recipient`, and no row is written. A participant cannot
tell a recipient it may not reach from one that is not there.

A delivery the receiving side refuses is rejected with `RejectNotAdmitted`,
reject code 5 — operation-specific, so above the generic codes
[`Query`](../../core-definitions/query.md) reserves — and the sender reads
`the recipient does not take messages from you`. It is a separate answer from
`route_not_found`, which the same node answers for an identity whose mailbox it
does not host and which a sender also reads when the answering node could not
be reached at all. The two are separate because the sender acts on them
differently: a sender turned away stops and asks whoever owns it, and a sender
that found nobody retries later.

**The code carries no reason.** [`auth`](../auth/README.md) answers one bit, so
a participant that admits nobody, an owner who does not admit this sender, and
an authority that would not decide all reach the sender as this one code.

**The code tells a sender that the node it reached hosts the target's
mailbox.** That is what separating the two answers costs, and the receiving
side pays it alone: a rejection is reachable only for an identity whose mailbox
the node hosts, so a sender whose own side admits every recipient learns which
mailboxes that node hosts. The sending side's refusal stays indistinguishable
from a name that resolves to nobody.

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

Mail never asks
[`mod.mcp.call_agent_action`](../mcp/types/mod.mcp.call_agent_action.md). That
action guards the [`mcp`](../mcp/README.md) endpoint's generic queries —
`astral-query` and declared tools — while the endpoint's mail tools reach this
module, which asks the two actions above.

## Delivery

A message is a row in the recipient's inbox. `messaging.send_message` puts a
`messaging.message` query to the recipient's identity carrying one
[`messaging.message`](types/messaging.message.md); the recipient's node stores
it and answers an `ack`. The node answers, not the participant, so delivery
finishes inside the resolve deadline whether or not anything reading the
recipient's mail is running, and a recipient on another node is the same call
as one on the same node.

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
never saw loses nothing.

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
room is marked `Truncated`. An identifier the participant does not hold is
reported rather than refused: one wrong identifier does not cost the rest of
the batch.

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
other query. A query addressed to an identity whose mailbox the node does not
host is answered `route_not_found` before anything else is asked. A query naming
any other path is answered `route_not_found` for a caller the mailbox's identity
admits: a mailbox is not a service. A caller it does not admit is rejected with
`RejectNotAdmitted` first, whatever the path: every query but a receipt asks
`mod.messaging.receive_action` before its path is read.

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

`messaging.list_messages` answers a participant's own rows and no other
participant's, whichever list it names. A row the receiving side rejected
carries the refusal, and a row a recipient's node refused after accepting the
delivery carries that node's own words. The second is quoted material and never
a field to act on. It is bounded where it is stored and marked where it was cut:
a refusing node decides neither how much of the reader's context it occupies nor
whether the reader can tell it read the whole of it.

**A collection is reported by the recipient's node.** When the body is handed
out and the same node hosts the sender's mailbox, that node stamps the sender's
row directly. When the sender is elsewhere, the recipient's node puts a
`messaging.receipt` query to the sender's identity carrying one
[`messaging.receipt`](types/messaging.receipt.md), and the sender's node stamps
the row and answers an `ack`.

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
case, not the edge one. A node holding no matching row answers an error, and a
node that does not host the target's mailbox answers `route_not_found`.

## Origin

Every operation rejects a query carrying the `network` origin, which a query
arriving over a [`Link`](../../core-definitions/link.md) carries, and a query
carrying the `mcp` origin, which a query the [`mcp`](../mcp/README.md) endpoint
puts for an agent carries — through `astral-query` or a declared tool. The
refusal comes before any action is submitted and before the caller is checked,
and a refused caller receives no bytes.

**The mail operations answer only a caller whose mailbox this node hosts.** Each
rejects a caller that is the zero identity or whose mailbox this node does not
host, as [Hosting](#hosting) defines it, before anything is read or written. The
node hosts no mailbox for its own identity, so a local caller that carries no
identity and acts as the node reaches no mailbox.

`messaging.create_identity` and `messaging.delete_identity` require
[`mod.auth.admin_manage_apps_action`](../auth/types/mod.auth.admin_manage_apps_action.md),
and `messaging.identity` requires
[`mod.auth.see_node_state_action`](../auth/types/mod.auth.see_node_state_action.md).
A participant holds neither by default.

`messaging.message` and `messaging.receipt` are not operations and take no such
refusal — each is addressed to a participant's identity rather than to a
node's, and a caller reaches both over a link. A node puts the deliveries and
receipts it sends with no origin: their path is fixed and addressed to a
participant, and no operation answers either name. Each is still checked for
hosting when it arrives.

**A participant reaches its own mail through apphost.** A participant's access
token is an [`apphost`](../apphost/README.md) access token, and apphost's
endpoints stamp no origin, so the token's bearer reaches the mail operations
there — and through them the participant's own mailbox and nothing else.

**An MCP tool carries no query.** The [`mcp`](../mcp/README.md) endpoint's mail
tools call the messaging module directly as the authenticated agent, so no
origin applies to them, and the module's hosting check does: a tool reaches a
mailbox only where the matching operation would.

## Configuration

The module reads `messaging.yaml`:

* `token_duration` – The lifetime of the access token
  `messaging.create_identity` issues when the caller names none. Defaults to 1
  year.
* `hosting_duration` – The lifetime of the hosting contract
  `messaging.create_identity` signs, counted from its signing. Defaults to 10
  years, the lifetime of the relay contract signed beside it.
* `delivery_timeout` – How long a node waits on one delivery or one receipt
  before it gives up. Defaults to 15 seconds.
* `wait_default` – The window `messaging.wait` grants a caller naming none.
  Defaults to 2 minutes.
* `wait_max` – The most any `messaging.wait` is granted. Defaults to 15 minutes.
* `max_payload_bytes` – The longest body, in bytes, a send accepts and a
  delivery stores. Defaults to 65536.
* `max_read_bytes` – The most body bytes one `messaging.read_messages` answer
  carries. Defaults to 65536.

**The deployment names both wait bounds.** What caps a held call is the
client's own request timeout and any proxy in front of it, which the node cannot
know.
