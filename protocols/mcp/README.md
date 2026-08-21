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
`mcp.list_agents` streams every record with its token. `mcp.set_visible` opens
or closes an agent. `mcp.delete_agent` removes one.

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

## Visibility

An agent is reachable by another caller only while its `Visible` flag is set. A
new agent is closed unless `mcp.create_agent` is given `visible`. A query
addressed to a closed agent is answered `route_not_found`. Closing an open
agent drops its queued queries and closes its live sessions, so the flag ends
conversations already under way.

The flag is the whole of an agent's reachability: the node knows no relation
between the agents it holds, so anything short of an explicit opt-in makes
every agent answerable to every other one and to the network.

## Delivery

A query addressed to a visible agent is accepted synchronously — the agent's
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
