# MCP Endpoint

The [`mcp`](../protocols/mcp/README.md) module serves mail tools and configured
Astral queries over streamable HTTP. Every call acts as the identity of its
bearer token.

## Authentication

The listener defaults to `tcp:127.0.0.1:8626`. It accepts any valid
[`apphost`](../protocols/apphost/README.md) access token; an agent record is
not required. Tokens from `messaging.create_mailbox` also work. Authentication
runs on every HTTP request. Revocation or expiry rejects later requests but
does not interrupt one already running.

## Mail tools

The five built-in tools call the messaging module directly as the authenticated
identity. They require its mailbox to be hosted on this node and expose no
delegated mailbox read or `peek` option.

| Tool | Operation | Result |
| --- | --- | --- |
| `send_message` | [`messaging.send_message`](../protocols/messaging/ops/messaging.send_message.md) | Sent message's `id`. |
| `list_messages` | [`messaging.list_messages`](../protocols/messaging/ops/messaging.list_messages.md) | Envelopes and paging cursors. |
| `read_messages` | [`messaging.read_messages`](../protocols/messaging/ops/messaging.read_messages.md) | Bodies, direct replies, and missing references. |
| `wait` | [`messaging.wait`](../protocols/messaging/ops/messaging.wait.md) | Matching inbox envelopes and wait timing. |
| `archive` | [`messaging.archive`](../protocols/messaging/ops/messaging.archive.md) | Whether the archive state changed; `undo` restores mail. |

The tools use JSON rather than Astral objects. Listings use `peer` for the other
party and `read` for inbox read state. IDs are hex text; timestamps are RFC 3339
text, omitted when unset. `wait` accepts `timeout_secs` and returns
`granted_secs` and `waited_secs` in whole seconds. The
[mailbox workflow](messaging.md#mailbox-use) and read effects are shared with
the operations.

`list_messages` and `wait` return `next_since` as decimal text: the greatest
cursor returned, or the input `since` when no newer row is returned. Supplying
`since`, including `"0"`, always produces `next_since` in normalized decimal.
Without `since`, an empty result omits it. Outbox and archive listings also
return their greatest cursor, but reject nonzero `since`.

`list_messages` passes `before` and `limit` to the operation. A full page with
`limit` returns its smallest cursor as `next_before`. No `next_before` is
returned without `limit`, with any supplied `since`, for the archive, or for a
short page. The next page uses that cursor with the same limit and filters.

Arguments are parsed before the module is called:

| Invalid value | Error |
| --- | --- |
| `since` outside decimal 0–9223372036854775807 | `since is a cursor a previous answer gave you, not "<since>"` |
| `before` outside that range | `before is a cursor a previous answer gave you, not "<before>"` |
| Negative `limit` | `limit is a number of messages, not <limit>` |
| `box` other than `inbox` or `outbox` | `box is inbox or outbox, not <box>` |
| ID other than 32 hex characters | `invalid message id` |

`read_messages` clamps negative `max_children` to 0 and values over 10 to 10;
the module treats 0 as 10. Other errors match the operations. An unhosted
caller receives `not a messaging participant`.

A waiting client that supplies an MCP progress token receives elapsed/granted
progress after each ten-second wait interval without a match. No token means
no progress notifications. There is no built-in tool that reports the caller's
own identity; a deployment can declare one.

## Declared tools

Each configured tool has a unique `name`, a `description`, and a fixed query
`astral://<identity-or-alias>:<query>`. It accepts no arguments. Built-in tool
names cannot be overridden. No tool accepts an arbitrary caller-written query.

The query's caller is the authenticated identity. The target service authorizes
it; the MCP endpoint submits no action of its own. The node routes on its own
context, preserving the caller through relay queries across links. The far node
admits the relay under the caller's relay contract.

An unresolved target returns `unknown target: <target>`; routing failure or
rejection returns `query failed: <error>`. The service defines the answer's
meaning. Unknown object types return as opaque bytes under their type names.
Responses are bounded by `query_timeout`, `max_response_bytes`, and
`max_response_objects`; reaching either size bound marks the answer `truncated`.

## Origin

Declared queries and activity reports carry `mcp` origin. The local shell
rejects that origin, so neither path reaches this node's operations. Across a
link, the far node stamps `network` origin; each target operation applies its
own origin and caller checks. MCP operations reject network queries.

These checks concern the query's entry path. Apphost endpoints stamp no origin
and accept the same access tokens. MCP management operations still require
their documented admin or state-reading action there. Mail tools call the
messaging module directly, so query-origin checks do not apply to them;
hosting, send, and receive checks do.

## Activity report

`activity_query` runs at the start of authenticated HTTP requests, regardless
of JSON-RPC method. It runs at most once per `activity_interval` per identity,
with at most one report in flight for that identity. The fixed query takes no
arguments, uses that identity as caller, and follows declared-tool routing.

The answer is read and discarded. Failure or timeout does not affect the HTTP
request and is not retried. Reports end at `query_timeout`. The target receives
activity for all authenticated identities across tenants, so it must be trusted
with that information.

## Configuration

`mcp.yaml` accepts these optional keys:

| Key | Default | Meaning |
| --- | --- | --- |
| `bind_mcp` | `tcp:127.0.0.1:8626` | Listener; empty disables HTTP while operations remain available. |
| `query_timeout` | `15s` | Declared-query and activity-report response window. |
| `max_response_bytes` | `65536` | Maximum bytes read from a declared-tool answer. |
| `max_response_objects` | `64` | Maximum objects decoded from a declared-tool answer. |
| `tools` | None | Declared tools, each with `name`, `description`, and `query`. |
| `activity_query` | Empty | Activity report query; empty disables reporting. |
| `activity_interval` | `1m` | Minimum interval between reports for one identity. |

Missing tool names or descriptions, duplicate/reserved names, and invalid tool
or activity query URLs prevent startup. Token lifetime, message size, read size,
and wait bounds belong to [messaging configuration](messaging.md#configuration).
