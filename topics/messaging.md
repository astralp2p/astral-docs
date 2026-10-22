# Messaging

The [`messaging`](../protocols/messaging/README.md) protocol stores mail for
identities. Each participant has an inbox for received messages and an outbox
for sent messages. Delivery succeeds when the recipient's node stores the
message; the recipient's client can be offline.

## Mailbox use

1. [`messaging.send_message`](../protocols/messaging/ops/messaging.send_message.md)
   sends a body to an identity or alias and returns a message ID.
2. [`messaging.list_messages`](../protocols/messaging/ops/messaging.list_messages.md)
   lists envelopes. [`messaging.wait`](../protocols/messaging/ops/messaging.wait.md)
   waits for matching inbox envelopes. Neither marks mail read.
3. [`messaging.read_messages`](../protocols/messaging/ops/messaging.read_messages.md)
   reads bodies by box and ID. An ordinary read of the owner's inbox marks mail
   read and reports collection to its sender. `peek` reads without those effects.
4. A reply uses the earlier message's ID as `ParentID`.
5. [`messaging.archive`](../protocols/messaging/ops/messaging.archive.md) hides
   completed mail from inbox/outbox listings and waits. `undo` restores it.

Waiting and reading claim no work: concurrent readers can receive the same
messages. Archiving changes only the owner's copy and sends no notification.
The `archive` list contains archived mail from both directions; each message
keeps its original `Box`. Archived messages remain readable by box and ID.

## Cursors and pages

An envelope's `Cursor` is a position in the node's write order, not a timestamp.
Clients keep their own cursors.

| Read | Arguments | Order |
| --- | --- | --- |
| Follow new inbox mail | `since=<greatest cursor seen>` | Oldest first |
| Page inbox or outbox history | `limit=1..100`, then `before=<smallest cursor returned>` | Newest first |
| Read archive | `list=archive`, optional `limit` | Newest first by creation time |

Nonzero `since` and `before` cannot be combined. The outbox and archive reject nonzero
`since`; the archive also rejects `before`. Without `limit`, a listing returns
all matching rows. An inbox listing without `before` or `limit` is oldest first.
With `since` and `limit`, it remains oldest first.

`messaging.wait` returns matching, unarchived inbox envelopes, including mail
already read. Passing its `NextSince` to the next call excludes earlier rows.
An empty answer repeats the input cursor. `Granted` is the allowed wait window;
`Waited` is the elapsed time; `TimedOut` means the window ended without a match.
The node accepts the query before waiting. Closing the channel cancels the wait.

## Replies and read bounds

`ParentID` names one earlier message; zero starts a new exchange. Both parties
must hold the parent in either box. Archived parents still count. A message
cannot name itself. Exchanges have no separate session record or expiry.

A read accepts 1–20 distinct `(Box, ID)` references and returns direct replies
one level deep. Repeated references are removed. `ChildIDs` lists all
unarchived direct replies of each named message, oldest first, regardless of
the requested reply mode:

* `none` returns no replies beside the named messages.
* `envelopes` returns replies without bodies; this is the default.
* `full` returns reply bodies and marks inbox replies read.

`MaxChildren` limits returned replies per named message to 10; zero also means
10. Missing references appear in `NotFound` without failing the batch.

`max_read_bytes` bounds the total body bytes. Each named body is charged before
its replies. A body omitted for space has `Content` null and `Truncated` true;
after the budget is exceeded, later bodies are omitted too. Read stamps and
collection reports happen before this budget check, including for omitted
bodies. A `peek` or [delegated read](mailbox-hosting.md#delegated-read) changes
no stamps, including on full replies.

## Configuration

`messaging.yaml` accepts these optional keys:

| Key | Default | Meaning |
| --- | --- | --- |
| `token_duration` | `8760h` | Default lifetime of a new mailbox's access token. |
| `delivery_timeout` | `15s` | Bounds sending a delivery or receipt and reading it at the receiving node. |
| `wait_default` | `2m` | Wait window when `timeout` is absent, zero, or negative. |
| `wait_max` | `15m` | Maximum wait window, including the default. Larger requests are clamped. |
| `max_payload_bytes` | `65536` | Maximum message body size. |
| `max_read_bytes` | `65536` | Maximum body bytes in one read result. |

Client and proxy timeouts can end a wait before its granted window.

Related topics: [Mailbox Hosting](mailbox-hosting.md),
[Message Delivery](message-delivery.md), [MCP Endpoint](mcp-endpoint.md).
