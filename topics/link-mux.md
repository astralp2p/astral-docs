# Link multiplexer protocol

A [*Link*](../core-definitions/link.md) is a live, authenticated, encrypted
connection between two [*Nodes*](../core-definitions/node.md). This document
specifies the wire protocol that runs *inside* a Link: how the two nodes
negotiate the multiplexer, how many query [*Channels*](../core-definitions/channel.md)
share the single encrypted stream, and the frames that carry them.

## Transport

A Link is established over any bidirectional bytestream — typically an
[*Exonet*](../core-definitions/exonet.md) connection, but any reliable,
ordered, full-duplex byte transport will do.

Establishment has three phases in strict order:

1. **Handshake** — a Noise XK handshake authenticates and encrypts the stream.
2. **Negotiation** — the parties agree on the multiplexer feature and mint a
   link identifier.
3. **Framing** — all subsequent bytes are multiplexer frames.

Nothing from a later phase may appear before the previous phase completes. An
interoperating implementation that skips or reorders these phases cannot
establish a Link.

## Handshake

The two parties run **Noise XK** over the raw bytestream. The static keys are
the nodes' [*Identity*](../core-definitions/identity.md) keys, so the pattern
authenticates each node under its network identity and encrypts everything that
follows.

The party that dials is the **initiator**; the party that accepts is the
**responder**. Under XK the responder's static key is known to the initiator up
front: the initiator commits to *which* responder Identity it intends to reach
before the handshake begins, and the handshake fails unless the responder proves
possession of that key. The responder learns the initiator's Identity during the
handshake. A node refuses to hand-shake with itself (equal static keys).

On success both sides hold an encrypted, authenticated stream and know each
other's Identity. Every byte described below travels inside that encrypted
stream.

The responder checks the initiator's Identity against its
[link admission](../protocols/nodes/README.md#link-admission) rules right after
the handshake. A refused initiator's connection is closed before Negotiation.

## Negotiation

Negotiation runs as a short [*Channel*](../core-definitions/channel.md) over the
encrypted stream, using the default binary encoding (each message is an
[*Object*](../core-definitions/object.md) framed as
`string8(ObjectType) ++ bytes32(Payload)`; see [Channel](../core-definitions/channel.md)).
It is symmetric to the handshake roles: the **responder** offers, the
**initiator** selects.

```
responder → initiator:  Uint16   feature count
responder → initiator:  String8  feature name    ×count
initiator → responder:  String8  selected feature
responder → initiator:  Uint8    status           (0 = accepted)
responder → initiator:  Nonce64  link id
```

1. The responder sends a [`uint16`](../primitive-types/uint16.md) count, then
   that many [`string8`](../primitive-types/string8.md) feature names. The only
   feature currently defined is `mux2`.
2. The initiator echoes back exactly one feature name — the one it selects. It
   must be a name from the offered list; the initiator selects `mux2`.
3. The responder replies with a [`uint8`](../primitive-types/uint8.md) status.
   `0` accepts the selection; any non-zero value rejects it and the Link is
   abandoned. A responder that does not recognise the selected feature answers
   non-zero.
4. On acceptance the responder sends a random [`nonce64`](../primitive-types/nonce64.md).
   This value is the **link id**: both sides retain it to name this Link (for
   example when [migrating](#migration) a session between Links).

An implementation cannot establish a Link without completing this exchange and
agreeing on `mux2`. After the link id is sent, the negotiation Channel ends and
the same encrypted stream carries multiplexer frames from both directions.

## Framing

The multiplexer runs a **binary [*Channel*](../core-definitions/channel.md)**
over the encrypted stream. Consequently a frame is *not* a compact numeric
opcode: it is an ordinary typed Object under the binary framing rules —

```
string8(FrameType) ++ bytes32(Payload)
```

Every frame on the wire is its [*Object Type*](../core-definitions/object-type.md)
name as a [`string8`](../primitive-types/string8.md), followed by the frame's
payload length-prefixed as [`bytes32`](../primitive-types/bytes32.md). The
payload bytes follow the [Binary Encoding](binary-encoding.md) (Big Endian,
fields in declared order). Both directions send frames; a Link is fully
symmetric once framing begins.

The frame types, by their wire type name and payload layout:

| Frame type                 | Payload fields (wire order)                                   |
|----------------------------|---------------------------------------------------------------|
| `nodes.frames.ping`        | `Nonce` nonce64, `Pong` [`bool`](../primitive-types/bool.md)  |
| `nodes.frames.query`       | `Nonce` nonce64, `Buffer` [`uint32`](../primitive-types/uint32.md), `Query` string (`uint16` length prefix) |
| `nodes.frames.relay_query` | `CallerID` [`Identity`](../core-definitions/identity.md), `TargetID` Identity, `Query` (an embedded `query` payload) |
| `nodes.frames.read`        | `Nonce` nonce64, `Len` uint32                                 |
| `nodes.frames.response`    | `Nonce` nonce64, `ErrCode` uint8, `Buffer` uint32             |
| `nodes.frames.data`        | `Nonce` nonce64, `Payload` bytes (`uint16` length prefix)     |
| `nodes.frames.migrate`     | `Nonce` nonce64                                               |
| `nodes.frames.reset`       | `Nonce` nonce64                                               |

Notes on the payload layouts:

* `Nonce` is a [`nonce64`](../primitive-types/nonce64.md): a 64-bit value, eight
  bytes Big Endian. In every frame it names the **session** (see below), except
  in `ping`/`pong` where it correlates a probe with its reply.
* `query.Query` and `data.Payload` carry their own 16-bit (`uint16`) length
  prefix inside the frame payload, so each is capped at 65 535 bytes on the wire.
  A single `query` string or `data` chunk never exceeds that. A query string
  over the cap is rejected before any frame is sent, with
  [*Reject Code*](../core-definitions/query.md) `2` (invalid query).
* `relay_query.Query` is the *payload* of a `query` frame embedded inline (the
  three fields `Nonce`, `Buffer`, `Query`); it carries no type tag of its own,
  because the outer `relay_query` frame already announced the type.
* `ping.Pong` false is a probe; the peer must answer with a `ping` bearing the
  same `Nonce` and `Pong` true. Pings double as the Link's keepalive (see
  [keepalive](#keepalive)).

## Keepalive

Both ends of every Link probe the peer while the Link is idle, so a Link whose
peer stops responding (a frozen process, a power cut, a dropped network) closes
in bounded time on every transport. The probes are the `ping` frames above; the
keepalive adds no frame.

Two durations time the keepalive of a Link:

* The **idle interval** `N`: a node probes the peer once `N` passes without a
  frame received from that peer.
* The **ping timeout** `T`: a node closes the Link when the `pong` for its
  probe does not arrive within `T`.

Each node runs the keepalive on its own:

* Every received frame restarts the idle interval, except a probe from the
  peer (`ping` with `Pong` false). A `pong`, a `query` and a `data` frame each
  restart it.
* A Link that carries frames from the peer more often than every `N` sends no
  probe.
* The ping timeout starts before the probe is written. A probe that cannot be
  written within `T`, because the peer stopped reading, closes the Link like a
  missing `pong`.
* A node that adds a Link to a peer while it holds other Links to that peer
  sends one probe on each of those older Links at once, whatever their idle
  interval. A new Link often means the peer moved and an older Link is dead.
  A dead older Link closes within its `T`; a healthy one answers and stays.
* Closing the Link tears down every session on it (see [sessions](#sessions)).
  A Link whose peer stopped responding therefore closes within `N + T` of the
  last frame received from that peer.
* On an idle healthy Link each end sends one probe and one `pong` per `N`.

`N` and `T` belong to the Link's transport: each transport sets its own pair,
and the two ends of one Link may use different pairs. A transport that sets
none gets `N` 15 s and `T` 10 s. The reference node reads the pair from the
transport module's config keys `link_idle_ping` and `link_ping_timeout`, with
these defaults:

| Transport | `N` | `T` |
|-----------|-----|-----|
| `tcp`     | 15 s | 10 s |
| `kcp`     | 10 s | 10 s |
| `gw`      | 20 s | 15 s |
| `tor`     | 30 s | 30 s |

The `kcp` idle interval is 10 s because a `kcp` Link rides a UDP NAT mapping.
On common NATs a fresh UDP mapping survives 15 s without traffic and is gone
by 30 s. A mapping that has carried traffic for a while lives several times
longer. A probe every 10 s keeps a fresh mapping open from the moment the Link
opens. Both ends probe, so traffic crosses the mapping in both directions.

## Sessions

Every routed [*Query*](../core-definitions/query.md) that travels over a Link
runs in its own **session**, keyed by a 64-bit nonce (the frame `Nonce`). One
session carries one query's [*Channel*](../core-definitions/channel.md): after
the query is accepted the session's `data` frames are the raw bidirectional
bytestream between caller and target.

Sessions are symmetric. Either node may open one at any time by sending a
`query` (or `relay_query`) frame with a fresh nonce; the initiator/responder
distinction from establishment does not restrict who opens sessions afterwards.
A node picks the nonce for sessions it opens, so both nonce spaces coexist on
one Link without collision.

Opening a session:

```
caller → target:  query{ Nonce, Buffer, Query }
target → caller:  response{ Nonce, ErrCode, Buffer }
```

The `Nonce` is chosen by the caller and names the session for its whole life.
The caller's `query.Buffer` advertises how many bytes of session data the caller
is initially willing to receive (its receive-buffer credit; see
[flow control](#flow-control)). The target's `response` closes the routing
step — see [response semantics](#response-semantics).

A session ends when either side sends a `reset` for its nonce, or when the Link
itself closes (which tears down every session on it). A query still waiting for
its `response` when the Link closes, or whose `query` frame the Link failed to
write, ends as unavailable (`7`) at once. A `data` or `read` frame
naming an unknown session provokes a `reset` back, so a stale sender learns the
session is gone. A `reset` for an unknown session is silently dropped (it
answers nothing, avoiding a reset loop).

## Flow control

Session data is **credit-based**. Neither side may send more session bytes than
the peer has said it can receive; credit is advertised up front and replenished
as the receiver drains its buffer.

* **Initial credit.** `query.Buffer` and the accepting `response.Buffer` each
  advertise the sender's own receive-buffer size — the number of `data` payload
  bytes the peer may send before waiting for more credit. (The reference buffer
  is 4 MiB.)
* **Replenishment.** As a receiver hands buffered bytes to its consumer, it
  sends `read{ Nonce, Len }` granting `Len` additional bytes of credit for that
  session. `Len` is the number of bytes just drained.
* **Sending.** A sender emits session bytes as `data{ Nonce, Payload }` frames,
  each chunk bounded by the credit outstanding for that session. A large write
  is split across several `data` frames (the reference chunk cap is 8 192 bytes,
  well under the 65 535-byte payload limit). When credit reaches zero the sender
  blocks until a `read` frame extends it.

The mechanism is per session, so a stalled session cannot starve the others
multiplexed on the same Link.

## Response semantics

A `response` frame carries the target's routing decision for the session named
by `Nonce`:

* **`ErrCode` == 0** — *accepted*. The session opens; `response.Buffer` seeds the
  caller's send credit, and from here the session's `data` frames are the
  query's bytestream in both directions.
* **`ErrCode` != 0** — *not accepted*. The session is discarded. The value
  names the cause:

| `ErrCode` | Meaning | The caller's node reads it as |
|-----------|---------|-------------------------------|
| `1` | refused: the target, a provider, or the relay refused the query | rejection with code `1` |
| `6` | timeout: the receiving node's own onward routing passed its deadline | rejection with code `6` |
| `7` | unavailable: the receiving node could not reach the next hop, or its router is not ready | rejection with code `7` |
| `255` | no route here: the receiving node found no route for the query | route not found |
| other | the target's own [*Reject Code*](../core-definitions/query.md) | rejection with that code |

* `255` is link-private. A receiving node that is handed a target's own `255`
  answers `1`, so `255` always means no route.
* A receiving node maps its routing failure to one value: a rejection keeps its
  code, a missing route is `255`, a passed deadline is `6`, and every other
  failure is `7`.
* The outcomes these values carry are defined in
  [Routing outcomes](../core-definitions/query.md#routing-outcomes).

The caller matches a `response` to its session by nonce and additionally checks
that it arrived from the expected peer before acting on it, so a response on the
wrong Link is ignored.

## Relay

A node can ask a peer to forward a query to a third node. The originator sends a
`relay_query` instead of a bare `query`:

```
relayer routes for the caller:
  caller  → relay:   relay_query{ CallerID, TargetID, query{ Nonce, Buffer, Query } }
  relay   → target:  (opens its own session toward TargetID)
  target  → relay → caller:  response{ Nonce, ErrCode, Buffer }
```

`relay_query` wraps the ordinary `query` payload with the **original** caller
and target [*Identities*](../core-definitions/identity.md), so the relaying node
knows on whose behalf it is acting and to whom.

The relaying node **authorizes** the relay before forwarding: unless the wrapped
`CallerID` is the peer that sent the frame, it must hold the
`mod.nodes.relay_for_action` authorization for that peer to relay on its behalf.
A `claimed` node also requires the peer to be a current member of its
[*Local Swarm*](../core-definitions/local-swarm.md), and checks that first
([App Routing](app-routing.md#authorizing-the-relay)).
If the relay is not permitted, the node answers the caller with a `response`
bearing the refused code (`1`) for the wrapped session's nonce and forwards
nothing.

## Migration

An open session's data stream can be handed off from one Link to another —
for example when a better [*Exonet*](../core-definitions/exonet.md) path appears
— without the caller or target observing a break. The hand-off is driven by the
`nodes.migrate_session` [*Operation*](../core-definitions/op.md), which
exchanges `mod.nodes.migrate_signal` messages (`ready`, `switched`, `resume`,
`done`; `ready` and `switched` carry the mover's remaining receive-buffer
credit) over a separate signalling
[*Channel*](../core-definitions/channel.md) between the two nodes; the target
Link is named by its [link id](#negotiation).

Within that dialogue, the `migrate` frame is the **delimiter on the data
stream**. Sent on the *old* Link for the session's nonce, it marks the exact
point after which no further `data` for that session will arrive on the old Link.
The receiver drains everything up to the `migrate` marker from the old Link, then
switches to reading that session's `data` from the new Link — so the byte stream
is continuous across the switch. A `migrate` frame for a session that is not in
the migrating state is ignored.
