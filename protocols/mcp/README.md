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

The endpoint serves six tools. `astral-query` sends a
[`Query`](../../core-definitions/query.md) to a node service. `astral-whoami`
returns the agent identity together with the host node and the node's
[`User`](../../core-definitions/user.md). The other four are the agent's mail:
`send_message` writes an [`mcp.message`](types/mcp.message.md) to another
agent, `inbox` lists the messages waiting without their bodies, `read_message`
reads one by [`mcp.message_id`](types/mcp.message_id.md), and `read_next` waits
for the oldest unread message and claims it.

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

The row carries the sender, the recipient, the body, the instant the message
arrived and the instant it was read. The sender is the query's caller and the
recipient its target. Neither is a field of the message, so a sender claims
neither.

**A message is read once.** `read_next` stamps the oldest unread message and
returns it, and a second reader takes the next message rather than the same
one. `read_message` opens one by identifier and stamps it read; reading is not
claiming, so a second read answers the same message unchanged.

**A delivery that arrives twice is stored once.** The
[`mcp.message_id`](types/mcp.message_id.md) is minted by the sender and keys
the row, so a sender that repeats a delivery after a lost `ack` leaves one
message.

An agent answers `mcp.message` and no other query. A query naming any other
path is answered `route_not_found`: an agent is a mailbox and not a service.

## Origin

Every operation is local-only: a query arriving over a
[`Link`](../../core-definitions/link.md) is rejected. `mcp.message` is no
operation and is not local-only — it is addressed to an agent's identity rather
than to a node's, and a caller reaches it over a link.

A query an agent sends through `astral-query` carries the `mcp` origin. The
[`shell`](../shell/README.md) protocol mounts every module's operations and
rejects a query carrying that origin, so an agent reaches neither the `mcp`
operations nor any other module's operations on its own host node. The four
operations answer a caller on the node itself — the operator, or the dashboard
that administers the agents.
