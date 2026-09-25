# mcp

The `mcp` protocol registers AI agents on a node and serves them the astral
network over the Model Context Protocol. An agent is a
[`messaging`](../messaging/README.md) participant: a node-minted
[`Identity`](../../core-definitions/identity.md), a signed relay
[`Contract`](../../core-definitions/contract.md), a signed hosting contract, an
optional [`Alias`](../../core-definitions/alias.md), and an
[`apphost`](../apphost/README.md) access token the agent presents as its bearer
credential, with an inbox and an outbox this node hosts. One node holds the
agents of many tenants and knows no relation between them.

Four operations manage agent records. `mcp.create_agent` mints an agent through
the messaging module, as `messaging.create_identity` mints a participant, keeps
its record, and returns its token. `mcp.agent` reads one record without its
token. `mcp.list_agents` streams every record with its token.
`mcp.delete_agent` removes one: the node revokes the agent's tokens and grants,
unsets its alias, withdraws its hosting of the agent's mailbox, deletes the mail
the agent owns there, and deletes the record.

## Endpoint

The MCP endpoint is a streamable HTTP listener configured by `bind_mcp`,
default `tcp:127.0.0.1:8626`; an empty value disables it. An agent
authenticates with its access token as a bearer token, and every tool call acts
as the authenticated agent identity. The endpoint accepts any unexpired
[`apphost`](../apphost/README.md) access token and reads no agent record, so a
participant minted with
[`messaging.create_identity`](../messaging/ops/messaging.create_identity.md)
authenticates as well. The token is checked on every HTTP request: a request
presenting a revoked or expired token is refused, and a request already running
is not cut short.

The endpoint serves six tools of its own. `astral-query` sends a
[`Query`](../../core-definitions/query.md) to a node service. The other five are
the agent's mail, and each adapts one [`messaging`](../messaging/README.md)
operation by a direct call to the messaging module, acting as the authenticated
agent:

* `send_message` – [`messaging.send_message`](../messaging/ops/messaging.send_message.md)
  writes a message to another identity and answers its `id`.
* `list_messages` – [`messaging.list_messages`](../messaging/ops/messaging.list_messages.md)
  lists a box without the bodies.
* `read_messages` – [`messaging.read_messages`](../messaging/ops/messaging.read_messages.md)
  reads whole messages by box and
  [`messaging.message_id`](../messaging/types/messaging.message_id.md).
* `wait` – [`messaging.wait`](../messaging/ops/messaging.wait.md) parks until a
  message arrives and answers what did.
* `archive` – [`messaging.archive`](../messaging/ops/messaging.archive.md) puts
  a message away, or back with `undo`.

A tool's arguments and answer are JSON shaped for the agent's model rather than
the operation's objects. A listing entry names the other party as `peer` and
says `read` rather than carrying the inbox stamps; identifiers are hex text,
instants are RFC 3339 text, and an unset instant is left out. `wait` takes
`timeout_secs` and answers `granted_secs` and `waited_secs` in whole seconds.
`list_messages` and `wait` answer `next_since`, the cursor to pass back as
`since`, as decimal text. A call that sent `since` — `0` included — is always
answered one: the greatest cursor answered, or the `since` it sent, read as a
number and written back in plain decimal, when nothing newer was answered. A
call that sent no `since` is answered the greatest cursor answered, and no
`next_since` when it answered nothing. An outbox or archive listing answers the
greatest cursor it listed as well, and both lists refuse a nonzero `since`.

A tool parses its arguments before it calls the module. A `since` that is not
a decimal integer from 0 to 9223372036854775807 is refused with
`since is a cursor a previous answer gave you, not "<since>"`, a `box` other
than `inbox` or `outbox` with `box is inbox or outbox, not <box>`, and a
message identifier that is not thirty-two hexadecimal characters with
`invalid message id`. `read_messages` reads a negative `max_children` as 0 and
one over 10 as 10. Beyond that, a tool refuses what its operation refuses, in the same words,
and answers `not a messaging participant` where its operation rejects a caller
whose mailbox this node does not host.

A tool call carries no query, so the origin refusal every `messaging` operation
applies reaches none of the five. The messaging module checks that this node
hosts the agent's mailbox, as it does for any caller, so a tool reaches a
mailbox only where the matching operation would.

**A held `wait` reports progress.** A caller that names an MCP progress token is
sent a progress notification each time the park passes its ten-second floor
with nothing new, carrying the time spent against the window granted. A client
bounds a call it hears nothing on, and the notification is what lets it spend
the window it was granted. A caller naming no token is sent nothing.

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

**A query leaves this node as a plain query.** `astral-query` and a declared
tool both route their query on a context naming the agent. A target on this
node reads the agent as the caller. A link carries such a query as a plain
query between the two nodes rather than as a relay query naming the agent and
the target, so the far node reads it as this node querying the far node.
[`messaging`](../messaging/README.md#delivery) routes its deliveries as the
node for this reason.

**The node reads none of the answer.** What the answer means belongs to the
answering service, and the description is declared beside the query for the same
reason. A type the node's registry does not hold is carried back as opaque bytes
under its type name rather than refused.

**A declared tool may not take one of the six names.** A configuration that
overrode one would silently repoint it, and the node refuses the configuration
instead. A name the endpoint does not serve is free.

## Authorization

What an agent may reach with a query is its owner's decision, and one node
carrying the agents of many tenants holds none of it: the endpoint asks
[`auth`](../auth/README.md) and acts on the answer.

`astral-query` and every declared tool submit
[`mod.mcp.call_agent_action`](types/mod.mcp.call_agent_action.md), with the
calling agent as actor and the query's target as `ToID`, before the
[`Query`](../../core-definitions/query.md) is built. A call the action refuses
is answered as one naming a target the node cannot resolve, `unknown target`.
An agent cannot tell a target it may not reach from one that is not there. What
the target does with a query that reaches it is the target's own decision.

Mail never asks this action. The five mail tools reach the messaging module,
which asks
[`mod.messaging.send_action`](../messaging/types/mod.messaging.send_action.md)
of the sender and
[`mod.messaging.receive_action`](../messaging/types/mod.messaging.receive_action.md)
of the recipient — see
[messaging § Authorization](../messaging/README.md#authorization).

## Origin

Every operation rejects a query that arrived over a
[`Link`](../../core-definitions/link.md).

A query an agent sends through `astral-query` or a declared tool carries the
`mcp` origin. The
[`shell`](../shell/README.md) protocol mounts every module's operations and
rejects a query carrying that origin, so an agent reaches no module's operations
by that path. Every [`messaging`](../messaging/README.md) operation rejects that
origin as well.

**The refusal reads the query's origin and never the caller.** Two paths stamp
one: a query arriving over a link carries `network`, and a query an agent sends
through `astral-query` or a declared tool carries `mcp`. A query arriving by
any other path carries no origin, and a query carrying no origin is not
refused. The node's own entry paths carry none,
[`apphost`](../apphost/README.md)'s endpoints among them, and an agent's access
token is an apphost access token and authenticates there.

An agent therefore reaches these four operations by a path the refusal does not
cover. `mcp.create_agent`, `mcp.list_agents` and `mcp.delete_agent` check the
caller as well: each requires
[`mod.auth.admin_manage_apps_action`](../auth/types/mod.auth.admin_manage_apps_action.md),
which an agent does not hold by default. `mcp.agent` answers no token.

## Configuration

The module reads `mcp.yaml`. Every key is optional, and a key left out takes its
default:

* `bind_mcp` – The endpoint the MCP server listens on. Defaults to
  `tcp:127.0.0.1:8626`; an empty value disables the endpoint, and the
  operations stay served.
* `query_timeout` – The response window of one `astral-query` call that names
  no `timeout_ms`, and of every declared tool call. Defaults to 15 seconds.
* `max_response_bytes` – The most bytes one `astral-query` or declared tool
  answer reads. Defaults to 65536; an answer that fills it is marked
  `truncated`.
* `max_response_objects` – The most objects one answer decodes. Defaults to 64;
  an answer that reaches it is marked `truncated`.
* `tools` – The [declared tools](#declared-tools), each a `name`, a
  `description` and a `query`. A node refuses to start on a tool with no name,
  no description, a taken name, or a query that is not
  `astral://<identity-or-alias>:<query>`.

The mail's own bounds — the access token's lifetime, the `wait` windows and the
longest body — are the [`messaging`](../messaging/README.md#configuration)
module's, in `messaging.yaml`.
