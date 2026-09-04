# mcp

The `mcp` protocol registers AI agents on a node and serves them the astral
network over the Model Context Protocol. An agent is a node-minted
[`Identity`](../../core-definitions/identity.md), a signed relay
[`Contract`](../../core-definitions/contract.md), an optional
[`Alias`](../../core-definitions/alias.md), and an
[`apphost`](../apphost/README.md) access token the agent presents as its bearer
credential. One node holds the agents of many tenants and knows no relation
between them.

Four operations manage agent records. `mcp.create_agent` mints an agent and
returns its token. `mcp.agent` reads one record without its token.
`mcp.list_agents` streams every record with its token. `mcp.delete_agent`
removes one.

## Endpoint

The MCP endpoint is a streamable HTTP listener configured by `bind_mcp`,
default `tcp:127.0.0.1:8626`; an empty value disables it. An agent
authenticates with its access token as a bearer token, and every tool call acts
as the authenticated agent identity.

The endpoint serves six tools of its own. `astral-query` sends a
[`Query`](../../core-definitions/query.md) to a node service. The other five are
the agent's mail: `send_message` writes an [`mcp.message`](types/mcp.message.md)
to another agent, `list_messages` lists a box without the bodies,
`read_messages` reads whole messages by [`mcp.message_id`](types/mcp.message_id.md),
`wait` parks until a message arrives and answers what did, and `archive` puts a
message away.

**An agent has three boxes and two of them are one axis.** `inbox` is what was
written to it and `outbox` what it wrote; `archive` is neither, because it is a
state rather than a direction — a message put away is still one the agent sent
or received, and both listings exclude it. A message is in exactly one of the
first two for its whole life, and moves into and out of the third.

`list_messages` names one of the three in `list`, and the narrowings belong to
the list named: an inbox narrows by who wrote and by what is unopened, an outbox
by who was written to and by what a recipient's node has stored and not handed
out. A narrowing that cannot apply to the named list is refused rather than
ignored, because ignoring it answers everything or nothing under a question the
caller thought it had asked.

**No tool names the agent to itself.** An agent's identity is minted by the node
and held by whoever registered the agent, and a node holding many tenants'
agents knows what none of them is called. A deployment that answers its agents
that question declares a tool for it.

## Declared tools

A deployment declares tools of its own beside the six. Each is a name, a
description, and one [`Query`](../../core-definitions/query.md) named as
`astral://<identity-or-alias>:<query>`. The node registers it under that name
and puts that query when an agent calls it.

**A declared tool takes no argument.** Its query is fixed where the tool is
declared, so what it asks does not vary with the call.

**The query is the agent's own.** It is put as the calling agent rather than as
the node, and it is the same
[`mod.mcp.call_agent_action`](types/mod.mcp.call_agent_action.md) that
`astral-query` raises about the same pair: a tool is a named query and buys the
agent no reach it did not have. It carries the `mcp` origin, so a tool named
against a node operation is refused as any agent's query to one is.

**The node reads none of the answer.** What the answer means belongs to the
answering service, and the description is declared beside the query for the same
reason. A type the node's registry does not hold is carried back as opaque bytes
under its type name rather than refused.

**A declared tool may not take one of the six names.** A configuration that
overrode one would silently repoint it, and the node refuses the configuration
instead. A name the endpoint served in an earlier revision and serves no longer
is free.

## Authorization

A call between two agents crosses two permissions, and each belongs to a
different party. The `mcp` protocol holds neither: one node carries the agents
of many tenants and knows no relation between them, so it asks
[`auth`](../auth/README.md) and acts on the answer.

The agent starting a call submits
[`mod.mcp.call_agent_action`](types/mod.mcp.call_agent_action.md) before the
[`Query`](../../core-definitions/query.md) is built. The agent being called
submits
[`mod.mcp.answer_agent_action`](types/mod.mcp.answer_agent_action.md) before
the message is accepted. A call proceeds only where both are granted.

A refused call is answered as one addressed to an identity the node holds no
agent for: `route_not_found` on the answering side, and an unresolvable target
on the calling side. A caller cannot tell an agent that refuses it from an
agent that does not exist, and an agent cannot tell a target it may not reach
from one that is not there.

**The node holds no reachability of its own.** An agent is reachable where a
registered handler, an active
[`Contract`](../../core-definitions/contract.md), or a configured external
authority says so, and a node with none of the three answers no call. What an
agent permits belongs to whoever owns it, and a node that held a copy would
hold a second answer to a question it does not decide.

A change of permission is answered on the next message the node asks about.
Nothing is in flight between two decisions: a message is a write that finishes
before its sender returns, so an owner narrowing what an agent may do has
nothing left to stop.

## Delivery

A message is a row in the recipient's inbox. `send_message` puts an
`mcp.message` query to the recipient's identity carrying one
[`mcp.message`](types/mcp.message.md); the recipient's node stores it and
answers an `ack`. The node answers, not the agent, so delivery finishes inside
the resolve deadline whether or not the recipient's model is running, and a
recipient on another node is the same call as one on the same node.

The row is an [`mcp.stored_message`](types/mcp.stored_message.md): the sender,
the recipient, the body, the message it answers, the instant the node wrote it,
the instant it was read and the instant it was put away. The sender is the
query's caller and the recipient its target. Neither is a field of the
[`mcp.message`](types/mcp.message.md) that carried it, so a sender claims
neither — the frame that crosses the link and the record the node keeps are two
types, and only the second names a party.

The stored instant is a claim about the node and not about the recipient, who
may not run for days. It is named for what the node did, beside a sender's row
whose own instants are named the same way.

## Replies

**A reply names the message it answers, and an exchange is a query.** An
[`mcp.message`](types/mcp.message.md) carries the identifier of the one message
it answers, and a message answering none carries the zero value. An exchange is
the chain those links make. Nothing is opened, owned, closed or expired, and no
node holds a record that another node must agree with.

**The link is a claim about another message, never about a party.** It is the
sender's, as the body is, while the sender and the recipient are the route's.
Naming a message means naming a 128-bit identifier that was never published, and
every row carries the identity of whoever wrote it.

**A reply names a message both parties hold.** The sending agent's node refuses
a parent that agent does not hold, and the recipient's node refuses one the
recipient does not hold. A message has one of each, so a parent is a message
between exactly these two parties, and no agent replies into an exchange it is
not part of. A message put away still counts as held: archiving does not unsee
it.

**That makes an exchange a forest.** Every parent names a message stored
earlier, so no chain of links returns to where it began and a reader walking one
needs no record of where it has been. A message naming itself is refused as the
cheapest case of the same rule.

**Thread is retired.** The flat label named what a reply now names for itself,
so it leaves rather than sitting dead on every message, and ParentID takes its
position in the frame. That is an incompatible change: the frame is positional
and carries no version marker, so a peer at the revision before it writes a
thread where a reader after it reads a parent, type-correct and silent. Nodes
carrying `mcp.message` between them move together.

**Replies are read, never followed.** `read_messages` answers a message with the
messages that name it, one level. Walking further is the reader's to do, and the
node holds no depth it must agree with anyone about.

## Reading

**Nothing is claimed.** `wait` parks until the agent's inbox holds a message it
has not put away, and answers what it found without touching a row. Two readers
waiting at once are answered the same messages, and neither takes anything from
the other. A reader that stops between the answer and the work leaves the
mailbox exactly as it was.

**A park names the window it was given.** `wait` takes the window the caller
asks for, grants it up to the deployment's ceiling, and answers `granted_secs`
beside `waited_secs` — the budget and the spend. An ask over the ceiling is
clamped rather than refused: a refusal would make the deployment's ceiling part
of every client's configuration, where a clamp is read off the answer. A caller
naming no window is granted the deployment's default. `timed_out` says the
granted window closed with nothing new.

**The inbox has a cursor and the node does not hold it.** Every answer that
lists the inbox carries `next_since`, and a caller passing it back as `since`
sees only what was written after. The cursor is a position in the order the node
wrote the rows, never an instant: a row's stored time is chosen before the row
commits, so a cursor over time steps past a message that had not appeared yet,
and does so permanently. An answer with nothing newer repeats the cursor it was
given, so following the instruction costs the caller no memory. The other two
lists are histories read newest first and refuse a cursor rather than answer one
wrongly.

**Reading is a separate act, and it is not a claim.** `read_messages` opens what
it is given and stamps each inbox message read. A second read answers the same
messages unchanged, so a caller that retries a call whose answer it never saw
loses nothing.

**A read answers the shape of an exchange and carries part of it.** Every
message a read answers names each of its direct replies in `child_ids`,
whatever else the answer carries: a reader that cannot see a reply exists cannot
ask for it, and a count names no message. How much of those replies comes back
beside it is the caller's — none, envelopes, or the bodies too. A reply's body
is opt-in because handing one out stamps it read and tells its sender it was
collected, which a reader asking about the parent never asked for.

**An answer is bounded, and says where the bound fell.** A read names at most
twenty messages and carries at most ten replies of each. The message the caller
named is charged against the response budget before its replies, so an overflow
drops what was not asked for first, and a message whose body was left out for
room is marked as such. An identifier the agent does not hold is reported rather
than refused: one wrong identifier does not cost the rest of the batch.

**Archiving is what says the agent is done.** `archive` stamps the message put
away, and a message put away is excluded from both listings and never answered
by `wait` again. It is the agent's own bookkeeping: it names no other node,
crosses no link, and the other party learns nothing from it. It is also the one
stamp with an inverse — `undo` puts the message back, through the same tool.

The answer is `changed` rather than `archived`, because under `undo` the second
would name the opposite of what happened: what the call reports is whether it
was the one that moved the message. It is false alike for a message already
where the caller asked and for one the caller does not hold, which the agent
acts on the same way — and separating them would say whether an identifier it
does not hold exists.

**A delivery that arrives twice is stored once.** The
[`mcp.message_id`](types/mcp.message_id.md) is minted by the sender and keys
the row, so a sender that repeats a delivery after a lost `ack` leaves one
message.

An agent answers `mcp.message` and `mcp.receipt`, and no other query. A query
naming any other path is answered `route_not_found`: an agent is a mailbox and
not a service.

## The sender's record

A send is a row in the sender's outbox, written before the delivery is
attempted and stamped by what the delivery returns. The two rows have different
owners: the recipient's row is the recipient's, and across nodes it is not on
the sender's machine at all, while what a sender knows survives whether or not
the recipient's node is reachable.

The row is an [`mcp.stored_message`](types/mcp.stored_message.md) in the outbox,
carrying the recipient, the body, and four instants — when the send was
attempted, when the recipient's node acknowledged the write, when the delivery
was known to have failed, and when the body was handed out. Each names when a
fact became true, and an unset instant is the absence of that fact rather than a
value somebody chose. A row nothing has stamped is a send whose fate is
unknown, which is the honest answer after a crash: an acknowledgement that
never arrived proves nothing about the write.

A send refused before delivery is attempted leaves no row: an unresolvable
recipient, `mod.mcp.call_agent_action` denied, a body over the bound, or a
parent the sending agent does not hold. A stored list of refusals would tell a
recipient that refuses apart from one that does not exist, which is the collapse
the refusal is built on.

`list_messages` answers an agent's own rows and no other agent's, whichever list
it names. The rejection an error carries is the recipient's node's own words, so
it is quoted material and never a field to act on. It is bounded where it is
stored and marked where it was cut: a refusing node decides neither how much of
the reader's context it occupies nor whether the reader can tell it read the
whole of it.

**A collection is reported by the recipient's node.** When the body is handed
out and the sender holds an agent on the same node, that node stamps the
sender's row directly. When the sender is elsewhere, the recipient's node puts
an `mcp.receipt` query to the sender's identity carrying one
[`mcp.receipt`](types/mcp.receipt.md), and the sender's node stamps the row and
answers an `ack`.

The stamp reports that the body was handed out and never that a model
considered it, and `wait` hands nothing out — a recipient learns a message
exists without its sender learning anything. A recipient that reads its mail and
stops marks every message it opened collected.

**A receipt is one attempt.** The fact it carries is already true and durable on
the node that sends it, so a receipt lost in transit leaves the sender believing
a message was never collected — wrong, permanently, and in the direction that
waits rather than the one that assumes. Nothing retries one, and the recipient's
read never waits on one.

**The outbox row is the receipt's permission.** The sender's node admits an
`mcp.receipt` without asking [`auth`](../auth/README.md): the row is the
consequence of a permitted past act, and the receipt says one thing about that
one message. Directions are granted per side and the two are independent, so
asking `mod.mcp.answer_agent_action` here would refuse a receipt wherever the
sender's inbound direction is narrower than its outbound one — the ordinary
case, not the edge one. A node holding no matching row answers an error, and a
node holding no sent rows at all answers `route_not_found`.

## Origin

Every operation rejects a query that arrived over a
[`Link`](../../core-definitions/link.md). `mcp.message` and `mcp.receipt` are no
operations and take no such refusal — each is addressed to an agent's identity
rather than to a node's, and a caller reaches both over a link.

A query an agent sends through `astral-query` carries the `mcp` origin. The
[`shell`](../shell/README.md) protocol mounts every module's operations and
rejects a query carrying that origin, so an agent reaches no module's operations
by that path.

**The refusal reads the query's origin and never the caller.** Two paths stamp
one: a query arriving over a link carries `network`, and a query an agent sends
through `astral-query` carries `mcp`. A query arriving by any other path carries
no origin, and a query carrying no origin is not refused. The node's own entry
paths carry none, [`apphost`](../apphost/README.md)'s endpoints among them, and
an agent's access token is an apphost access token and authenticates there.

An agent therefore reaches these four operations by a path the refusal does not
cover. `mcp.list_agents` answers every registered agent's access token to
whoever reaches it, and `mcp.delete_agent` takes an alias, which an agent reads
off any message it holds. Restricting the four to an operator is a caller-identity
check, which the protocol does not currently define.
