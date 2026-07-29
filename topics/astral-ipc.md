# apphost IPC protocol

The astral node exposes an IPC surface (`mod/apphost`) that lets local
processes route outbound queries through the node and serve inbound queries
targeting an identity the process owns. This document specifies the wire
protocol.

## Transport

The host listens on one or more endpoints of the form `<proto>:<addr>`. The
defaults are:

| Endpoint                | Notes                                  |
|-------------------------|----------------------------------------|
| `tcp:127.0.0.1:8625`    | loopback TCP                           |
| `unix:~/.apphost.sock`  | unix domain socket                     |
| `memu:apphosty`         | in-process pipe, unbuffered            |
| `memb:apphostb`         | in-process pipe, buffered              |

The two `mem` endpoints are in-process pipes. They are reachable only from code
embedded in the same process as the node — a binding linked into the host
application — and not from a separate process, so a command-line client cannot
dial them.

All endpoints carry the same protocol. A guest opens a fresh connection per
session; a session is one outbound query, one service registration, or one
inbound-query attach.

## Framing

The IPC protocol uses a binary [channel](../core-definitions/channel.md) for
messages.

## Session handshake

1. Guest connects. Host sends `mod.apphost.host_info_msg{Identity, Alias}` —
   the node's identity and local alias.
2. *(optional)* Guest sends `mod.apphost.auth_token_msg{Token}`. Host replies
   with `mod.apphost.auth_success_msg{GuestID}` on success or
   `mod.apphost.error_msg{auth_failed}` on failure.

After step 1 the guest is *anonymous*; after a successful step 2 the session
is bound to `GuestID`. Anonymous guests:

- may send queries only if the host's `AllowAnonymous` config is on (default);
- have the network [`Zone`](../core-definitions/zone.md) (`ZoneNetwork`) stripped from their queries, so they cannot reach other nodes;
- may not register handlers.

A query with a zero `Caller` is routed as the node's own identity. The host
tags every query from a token-less session as anonymous so an operation can
tell an anonymous caller apart from the node itself once the caller is resolved.
IPC guests carry no web origin and are not subject to the web-guest operation
allowlist that applies to browser guests (see the apphost protocol).

The guest may then send exactly one of `RouteQueryMsg`, `RegisterServiceMsg`,
or `AttachQueryMsg` (the last only on a fresh sub-connection answering an
`IncomingQueryMsg`). Any other top-level message yields
`error_msg{protocol_error}` and connection close.

## Sending queries

```
guest → host:  mod.apphost.route_query_msg {
                 Nonce:   Nonce,
                 Caller:  Identity,         // may be zero
                 Target:  Identity,
                 Query:   String16,
                 Zone:    Zone,             // dvn / device / network / virtual
                 Filters: []String8,        // optional
               }
host  → guest: one of:
                 mod.apphost.query_accepted_msg {}
                 mod.apphost.query_rejected_msg { Code: Uint8 }
                 mod.apphost.error_msg         { Code: String8 }
```

Caller authorization:

- zero `Caller` → anonymous;
- `Caller == GuestID` → allowed;
- otherwise the guest must hold a `SudoAction` for `Caller`, else
  `error_msg{denied}`.

Error codes returned for `route_query`: `route_not_found`,
`target_not_allowed`, `canceled`, `timeout`, `internal_error`, `denied`.

On `query_accepted_msg` the connection ceases to be a message channel and
becomes the **raw bidirectional bytestream of the accepted query**. Both
endpoints write/read query bytes directly; the session ends when either side
closes the connection. One query per connection.

A query in flight can be cancelled by opening a separate session and routing
`apphost.cancel?id=<Nonce>` to the host.

## Receiving queries

There are two ways to register as a handler for an identity. Both require an
authenticated session and the same authorization: the registered identity
must equal `GuestID`, or the guest must hold a `SudoAction` for it.

### A. Register-service (push notifications on the registration conn)

```
guest → host:  mod.apphost.register_service_msg { Identity }
host  → guest: ack                              (or error_msg{denied})
```

The registration connection stays open. For each inbound query targeting
[`Identity`](../core-definitions/identity.md), the host pushes:

```
host → guest: mod.apphost.incoming_query_msg {
                QueryID: Nonce,
                Caller:  Identity,
                Target:  Identity,
                Query:   String16,
              }
```

Within `QueryAttachTimeout` (5 s) the guest must do one of:

- **Accept** — open a *new* IPC connection, complete the handshake (no
  `AuthTokenMsg` needed: `QueryID` is the pairing token), and send:

  ```
  guest → host: mod.apphost.attach_query_msg { QueryID }
  host  → guest: ack              (or error_msg{route_not_found} if QueryID
                                   is unknown/expired)
  ```

  After the `Ack` this connection becomes the raw bytestream of the inbound
  query, with the guest as responder.

- **Reject** — send on the *registration* conn:

  ```
  guest → host: mod.apphost.reject_incoming_msg { QueryID, Code: Uint8 }
  ```

  The caller observes `query_rejected_msg{Code}`.

- **Ignore** — after the timeout the caller observes `route_not_found`.

Closing the registration connection unregisters the handler.

### B. Register-handler (host dials a guest-side IPC endpoint)

The guest issues a normal `route_query` to the host with method
`apphost.register_handler`:

```
Query: "apphost.register_handler?endpoint=<proto>:<addr>&token=<Nonce>"
```

On `query_accepted_msg` the host sends `ack` over the resulting
bytestream and registers the handler. The host keeps the handler in its
registry; the original query conn is closed.

For each inbound query targeting `GuestID`, the host **dials `endpoint` as a
fresh IPC connection** and sends:

```
host    → handler: mod.apphost.handle_query_msg {
                     IpcToken: Nonce,         // == registered token
                     ID:       Nonce,         // query nonce
                     Caller:   Identity,
                     Target:   Identity,
                     Query:    String16,
                   }
handler → host:    one of:
                     ack                            (accept)
                     mod.apphost.query_rejected_msg { Code: Uint8 }
                     mod.apphost.error_msg          { Code: String8 }
                     (or close) ─────────────────────── route_not_found to caller
```

On `Ack` the dialed connection becomes the raw bytestream for that query.
The handler must therefore listen on `endpoint` (any `tcp` / `unix` / `memu`
/ `memb` address it owns) before registering.

Lifecycle:

- A failed dial removes the handler from the registry.
- For explicit, immediate cleanup the guest may open a session, route
  `apphost.bind`, send `mod.apphost.bind_msg{Token}` on the resulting
  bytestream, and keep that bind connection open. When the bind connection
  closes, every handler registered with that `Token` is removed.

## Error codes (`mod.apphost.error_msg.Code`)

| Code                 | Meaning                                            |
|----------------------|----------------------------------------------------|
| `auth_failed`        | invalid `AuthTokenMsg`                             |
| `denied`             | guest lacks the required authorization             |
| `route_not_found`    | no handler accepted the query                      |
| `target_not_allowed` | caller may not query this target                   |
| `canceled`           | query was cancelled                                |
| `timeout`            | query timed out                                    |
| `protocol_error`     | unexpected/invalid message; connection is closed   |
| `internal_error`     | catch-all                                          |
