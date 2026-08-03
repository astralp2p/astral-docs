# WebSocket transport (astral-js)

How `astral-js` sends and receives queries against the local astrald node
over the apphost WebSocket endpoint. Covers the WS transport only — query
semantics, identities and the broader apphost protocol live elsewhere.

The client described below uses the `astral.json.v1` subprotocol.

## Server surface

The `/.ws` upgrade negotiates one of two subprotocols via the
`Sec-WebSocket-Protocol` header:

- `astral.binary.v1` — binary WebSocket frames carrying the standard
  [binary-channel](../core-definitions/channel.md) bytestream.
- `astral.json.v1` — one JSON envelope per text frame.

The connection is closed with `StatusPolicyViolation` (1008) if neither
subprotocol is offered.

Any `Origin` is accepted at the WebSocket layer — the endpoint is
loopback-only at the network layer, so a remote page cannot reach it
regardless of `Origin`. The HTTP `Authorization: Bearer` header used by the
rest of the HTTP bridge is not consulted for `/.ws`; authentication uses the
in-protocol auth token message.

## Endpoint and framing

- URL: the apphost HTTP listener exposes a WebSocket upgrade at `/.ws`
  (default `ws://127.0.0.1:8624/.ws`). Loopback-only; no TLS.
- Subprotocol: the client always negotiates `astral.json.v1` via
  `Sec-WebSocket-Protocol`. Every frame is one text message containing a
  JSON envelope:

  ```json
  { "Type": "mod.apphost.<name>", "Object": { ... } }
  ```

  The library presents this to user code as a friendly `AstralObject`
  `{ type, value }` and converts between the two on the wire.

Binary frames are silently dropped by the receiver — this client is
text/JSON only.

## Connection lifecycle

`connect(url, { token })` opens a short-lived WS, runs the handshake to
capture host info, and immediately closes it. The returned `Host` holds the
URL, token and host identity, and opens a **fresh WebSocket per query and
per registration**. There is no persistent multiplexed session.

Handshake on every WS opened by the library:

1. Open WS with subprotocol `astral.json.v1`.
2. Server pushes `mod.apphost.host_info_msg` → `{ Identity, Alias }`.
3. If a token was supplied, client sends `mod.apphost.auth_token_msg`
   → `{ Token }`. Server replies with either
   `mod.apphost.auth_success_msg` → `{ GuestID }` or
   `mod.apphost.error_msg` (`AuthError`).
4. The WS is now ready for one query or one registration.

Per-query WSes opened by `IncomingQuery.accept()` skip step 3 — the
unguessable `QueryID` is the pairing token.

## Sending queries (outbound)

```js
const stream = await host.query('user.info', {
  args: { name: 'alice' },          // appended as ?name=alice
  target:  null,                    // default: host.identity
  caller:  undefined,               // default: host.guestID
  zone:    'dvn',
  filters: null,
});

for await (const { type, value } of stream) { /* ... */ }
stream.close();                     // idempotent; closes the WS
```

What happens on the wire:

1. The library opens a new WS and completes the handshake.
2. It sends `mod.apphost.route_query_msg` with a fresh 16-hex-character
   `Nonce`, `Caller`, `Target`, [`Query`](../core-definitions/query.md) (with `?args` merged in), `Zone`
   and `Filters`.
3. The server replies with exactly one of:
   - `mod.apphost.query_accepted_msg` → the WS becomes the query
     bytestream and `host.query` resolves to a `Stream`.
   - `mod.apphost.query_rejected_msg` → throws `QueryRejected{code}`.
   - `mod.apphost.error_msg` with code `route_not_found` → throws
     `RouteNotFound`; any other code → `ProtocolError`.
4. After acceptance, both peers exchange `AstralObject` frames freely. The
   stream ends at the first [`eos`](../primitive-types/eos.md) frame or when the WS closes; the async
   iterator returns at that point. `stream.send(obj)` writes a frame;
   `stream.close()` tears down the WS (which cancels the query host-side).

Notes:

- One query per WS. Multiple concurrent queries means multiple WSes.
- `caller` defaults to the connection's `guestID`; passing `null`
  explicitly suppresses it (the host then fills in its own node identity,
  which is rarely what you want).
- an unauthenticated web guest may call only the operations on the node's
  claim-state allowlist — the setup-ceremony operations while the node is
  unclaimed, otherwise a minimal identity-acquisition set. [Operations](../core-definitions/op.md) outside
  it are rejected. Authenticating lifts the restriction. See the apphost
  protocol.
- JSON mode auto-injects `out=json&in=json` server-side so responder
  frames are JSON-encoded `astral.JSONAdapter` objects. Override by
  putting `in=`/`out=` in `queryString` yourself. Responders that bypass
  the channel and write raw bytes are not safe for JSON mode; query them
  over `astral.binary.v1`.

## Receiving queries (inbound)

```js
const reg = await host.register(identity, async (q) => {
  if (q.query.startsWith('forbidden')) return q.reject(1);
  const s = await q.accept();
  s.send({ type: 'string8', value: 'hi ' + q.caller });
  s.send({ type: 'eos' });
  s.close();
});
// later:
reg.unregister();
```

Two WSes are involved:

**Registration WS** — long-lived, one per registered identity.

1. Opened and handshaken by `host.register(identity, handler)`.
2. Client sends `mod.apphost.register_service_msg` → `{ Identity }`.
3. Server replies with [`ack`](../primitive-types/ack.md); on error it sends `mod.apphost.error_msg`
   (e.g. unauthorized). Authorization mirrors `route_query`: the caller
   identity must equal [`Identity`](../core-definitions/identity.md) or hold a `SudoAction` for it.
4. The library then loops on the receiver. Stray frames are ignored;
   every `mod.apphost.incoming_query_msg`
   (`{ QueryID, Caller, Target, Query }`) is wrapped in an
   `IncomingQuery` and handed to `handler`.
5. `reg.unregister()` (or `close` from the server / network) closes the
   WS and ends the registration.

**Per-query WS** — short-lived, one per accepted inbound query.

- `q.accept()` opens a new WS, **skips auth** (the `QueryID` is the
  pairing token), then sends `mod.apphost.attach_query_msg` →
  `{ QueryID }` and waits for `ack` (an `error_msg` here means the
  `QueryID` is unknown or expired and surfaces as `ProtocolError`).
- The resolved `Stream` is the responder side. Use `s.send({type,value})`
  to write frames; conventionally finish with `{ type: 'eos' }` followed
  by `s.close()`.
- `q.reject(code = 1)` sends `mod.apphost.reject_incoming_msg`
  → `{ QueryID, Code }` on the **registration** WS — no per-query WS is
  opened. `code` must be in the range 1–255.
- `accept` and `reject` are one-shot; either must occur within the host's
  5-second attach timeout, otherwise the caller sees `route_not_found`.

If the handler throws, the library calls `q.reject(0xff)` and logs the
error to the console. Make sure that fallback is acceptable, or catch
inside the handler.

## Streams

`Stream` is returned by both `host.query` (caller side) and
`q.accept` (responder side); it wraps one WS.

- `stream.send(obj)` — write one `AstralObject` frame. Throws if the
  stream has been closed locally.
- `for await (const obj of stream)` — async-iterate received frames. The
  iterator returns when an `eos` frame arrives or when the WS closes.
- `stream.close()` — close the underlying WS. Idempotent; safe to call
  even after the peer has closed.

Both directions share the same envelope. There is no flow control or
back-pressure beyond what the WebSocket layer provides.

## Errors

Thrown by `connect`, `host.query`, `host.register` and `q.accept`:

| Class             | When                                                      |
|-------------------|-----------------------------------------------------------|
| `ConnectError`    | WS failed to open or closed before the expected reply.    |
| `AuthError`       | Server returned `error_msg` in response to the auth token.|
| `QueryRejected`   | Server returned `query_rejected_msg` (`.code` is numeric).|
| `RouteNotFound`   | Server returned `error_msg{Code:'route_not_found'}`.      |
| `ProtocolError`   | Unexpected message type or unknown error code.            |

All are exported individually and on the `errors` namespace.
