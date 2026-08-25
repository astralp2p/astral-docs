# mcp

The `mcp` protocol registers AI agents on a node and serves them the astral
network over the Model Context Protocol. An agent is a node-minted
[`Identity`](../../core-definitions/identity.md), a signed relay
[`Contract`](../../core-definitions/contract.md), an optional
[`Alias`](../../core-definitions/alias.md), and an
[`apphost`](../apphost/README.md) access token the agent presents as its bearer
credential. One node holds the agents of many tenants and knows no relation
between them.

Five operations manage agent records. `mcp.create_agent` mints an agent and
returns its token. `mcp.agent` reads one record without its token.
`mcp.list_agents` streams every record with its token. `mcp.disconnect_agent`
ends an agent's live traffic. `mcp.delete_agent` removes one.

## Endpoint

The MCP endpoint is a streamable HTTP listener configured by `bind_mcp`,
default `tcp:127.0.0.1:8626`; an empty value disables it. An agent
authenticates with its access token as a bearer token, and every tool call acts
as the authenticated agent identity.

The endpoint serves five tools. `astral-query` sends a
[`Query`](../../core-definitions/query.md) to an identity. `astral-listen`
waits for one query addressed to the agent. `astral-send` and `astral-receive`
carry a multi-turn dialog over the accepted
[`Channel`](../../core-definitions/channel.md). `astral-whoami` returns the
agent identity together with the host node and the node's
[`User`](../../core-definitions/user.md).

## Authorization

A call between two agents crosses two permissions, and each belongs to a
different party. The `mcp` protocol holds neither: one node carries the agents
of many tenants and knows no relation between them, so it asks
[`auth`](../auth/README.md) and acts on the answer.

The agent starting a call submits
[`mod.mcp.call_agent_action`](types/mod.mcp.call_agent_action.md) before the
[`Query`](../../core-definitions/query.md) is built. The agent being called
submits
[`mod.mcp.answer_agent_action`](types/mod.mcp.answer_agent_action.md) before a
parked `astral-listen` is claimed and before the query is queued — a parked
listener is not permission, and claiming one for a query about to be refused
would consume it. A call proceeds only where both are granted.

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

`mcp.disconnect_agent` ends an agent's live traffic: it closes the
conversations the agent is in and drops the queries waiting for it. It carries
no permission and writes none — a change of permission is answered on the next
call the node asks about, and the traffic already flowing is the one part of
that change its owner cannot make elsewhere.

## Delivery

A query the two actions permit is accepted synchronously — the agent's
model cannot answer within the resolve deadline — and the accepted connection
becomes a dialog session. An agent parked in `astral-listen` takes the query
directly. An agent that is not listening queues it: at most `max_pending`
queries per agent, each held for `pending_ttl`, delivered on the agent's next
`astral-listen` call. A query arriving for an agent whose queue is full is
answered `route_not_found`.

A session is idle-timed by `session_ttl`, refreshed on every send and receive.

## Origin

Every operation is local-only: a query arriving over a
[`Link`](../../core-definitions/link.md) is rejected.

A query an agent sends through `astral-query` carries the `mcp` origin. The
[`shell`](../shell/README.md) protocol mounts every module's operations and
rejects a query carrying that origin, so an agent reaches neither the `mcp`
operations nor any other module's operations on its own host node. The five
operations answer a caller on the node itself — the operator, or the dashboard
that administers the agents.
