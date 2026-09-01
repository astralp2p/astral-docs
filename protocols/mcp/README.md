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
instead. A name the endpoint has retired is reserved on the same terms: an agent
that learned what a name meant must not find a deployment answering it with
something else.

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

The row carries the sender, the recipient, the body, the message it answers, the
instant the node wrote it, the instant it was read and the instant it was put
away. The sender is the query's caller and the recipient its target. Neither is
a field of the message, so a sender claims neither.

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

**A parent the node does not hold is stored as it stands.** A message may name
one that never arrived, one that was put away, or one that never existed, and
the recipient's node neither refuses it nor repairs it: a claim about a message
nobody has is a claim nothing answers, and a link that leads nowhere costs the
message beside it nothing. The one link refused is a message naming itself.

**Replies are read, never followed.** `read_messages` answers a message with the
messages that name it, one level. Walking further is the reader's to do, and the
node holds no depth it must agree with anyone about.

## Reading

**Nothing is claimed.** `wait` parks until the agent's inbox holds a message it
has not put away, and answers what it found without touching a row. Two readers
waiting at once are answered the same messages, and neither takes anything from
the other. A reader that stops between the answer and the work leaves the
mailbox exactly as it was.

**Reading is a separate act, and it is not a claim.** `read_messages` opens what
it is given and stamps each inbox message read. A second read answers the same
messages unchanged, so a caller that retries a call whose answer it never saw
loses nothing.

**Archiving is what says the agent is done.** `archive` stamps the message put
away, and a message put away is excluded from both listings and never answered
by `wait` again. It is the recipient's own bookkeeping: it names no other node,
crosses no link, and the sender learns nothing from it.

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

The row carries the recipient, the body, and four instants — when the send was
attempted, when the recipient's node acknowledged the write, when the delivery
was known to have failed, and when the body was handed out. Each names when a
fact became true, and an unset instant is the absence of that fact rather than a
value somebody chose. A row nothing has stamped is a send whose fate is
unknown, which is the honest answer after a crash: an acknowledgement that
never arrived proves nothing about the write.

A send refused before delivery is attempted — an unresolvable recipient, or
`mod.mcp.call_agent_action` denied — leaves no row. A stored list of refusals
would tell a recipient that refuses apart from one that does not exist, which is
the collapse the refusal is built on.

`list_messages` answers an agent's own rows and no other agent's, whichever box
it names. The rejection an error carries is the recipient's node's own words, so
it is quoted material and never a field to act on.

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

Every operation is local-only: a query arriving over a
[`Link`](../../core-definitions/link.md) is rejected. `mcp.message` and
`mcp.receipt` are no operations and are not local-only — each is addressed to an
agent's identity rather than to a node's, and a caller reaches both over a
link.

A query an agent sends through `astral-query` carries the `mcp` origin. The
[`shell`](../shell/README.md) protocol mounts every module's operations and
rejects a query carrying that origin, so an agent reaches neither the `mcp`
operations nor any other module's operations on its own host node. The four
operations answer a caller on the node itself — the operator, or the dashboard
that administers the agents.
