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
| `nodes.frames.close`       | `Reason` [`uint8`](../primitive-types/uint8.md)               |

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
* `close.Reason` names why the sender closes the Link:

  | `Reason` | Name       | Meaning |
  |----------|------------|---------|
  | `0`      | `closed`   | the sender closes the Link for a cause no other value names |
  | `1`      | `excess`   | the sender keeps another Link to the same peer and closes this one |
  | `2`      | `shutdown` | the sender's node is shutting down |

  The set is append-only: a later revision adds values and never changes or
  reuses these. A receiver treats a `Reason` it does not know as `closed`.

## Close notice

A node that closes a Link sends one `close` frame first, so the peer learns of
the close at once instead of when its [keepalive](#keepalive) gives up. A
transport that carries no end-of-stream signal, such as `kcp`, needs it most.

* **Receiver.** A node that receives `close` closes its end of the Link and
  tears down every session on it (see [sessions](#sessions)). It sends nothing
  back; in particular it never answers with a `close` of its own.
* **Best effort.** The sender writes the frame within a bounded time and closes
  the Link whether or not the write finished. A peer that never reads delays the
  close by at most that bound. The reference bound is 1 s (`closeNoticeBound`).
  The peer can still miss the frame, so the keepalive stays the backstop.
* **Simultaneous close.** Both ends can close the same Link at once, so each
  sends `close` and each receives the other's. A node that already closes the
  Link ignores a `close` it receives, and sends nothing in return. Both ends
  end the Link once.
* **No frame.** A node sends no `close` when:
  * the Link has already ended on its side: the transport reported
    end-of-stream or an error, a frame could not be decoded, or the peer's
    `close` arrived (the Link is the peer's to end, so nothing is echoed);
  * the Link was already closing: only the first close of a Link sends the
    frame;
  * the connection never became a Link, because the handshake or the
    negotiation failed before the framing phase;
  * the node stops without closing its Links: a killed process, a power cut,
    or a dropped network sends nothing, and the peer's keepalive detects it.

  A write that is blocked when the bound ends sends no complete frame either.
  That is the usual outcome of a [write stall](#write-stall): the `close` write
  queues behind the stuck write, so the peer learns of the close through the
  transport or its keepalive.
* **Closing Links only.** A node sends `close` only on a Link it closes. It
  never sends `close` on a Link it keeps, including the Link it keeps when it
  closes an `excess` one.
* **Mixed versions.** A receiver that has no `nodes.frames.close` type cannot
  decode the frame. The reference node ends such a Link on any frame type it
  cannot decode, so the receiver closes the Link. The sender closes the same
  Link, so the outcome equals the close the frame announces.

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
* Closing the Link tears down every session on it (see [sessions](#sessions)).
  A Link whose peer stopped responding therefore closes within `N + T` of the
  last frame received from that peer, plus the slack described under
  [detection bound](#detection-bound).
* On an idle healthy Link each end sends one probe and one `pong` per `N`.

### Per-transport values

`N` and `T` belong to the Link's transport: each transport sets its own pair,
and the two ends of one Link may use different pairs. The reference node reads
the pair from the transport module's config keys `link_idle_ping` and
`link_ping_timeout`. A transport that sets none (a key left at 0, or a conn
that reports no keepalive) gets the pair of its network's **transport profile**
(`TransportProfile`: `IdlePing`, `PingTimeout`); a network without a profile
gets `N` 15 s and `T` 10 s. The transport's own pair wins over the profile.

| Transport | `N` (config default) | `T` (config default) | Bound `N + T` | Profile `N` / `T` |
|-----------|----------------------|----------------------|---------------|-------------------|
| `tcp`     | 15 s | 10 s | 25 s | 15 s / 10 s |
| `kcp`     | 10 s | 10 s | 20 s | 10 s / 10 s |
| `gw`      | 20 s | 15 s | 35 s | 15 s / 10 s |
| `tor`     | 30 s | 30 s | 60 s | 15 s / 10 s |

The bound is the longest time a dead Link stays open after the last frame
received from its peer, with a node running the default pair of its transport.
A node that sets another pair has the bound of that pair. The `gw` and `tor`
config defaults are larger than their profile, so the profile applies only
where the config gives 0.

* `kcp` rides UDP, which never reports a broken connection, so a `kcp` Link
  relies entirely on the keepalive (and on a received `close`) to end. The
  `kcp` idle interval is 10 s because a `kcp` Link rides a UDP NAT mapping.
  On common NATs a fresh UDP mapping survives 15 s without traffic and is gone
  by 30 s. A mapping that has carried traffic for a while lives several times
  longer. A probe every 10 s keeps a fresh mapping open from the moment the Link
  opens. Both ends probe, so traffic crosses the mapping in both directions.
* A `tcp` Link also ends when the OS reports the connection broken, which can
  precede the bound; a `tor` Link may stay open for up to 60 s after a peer
  vanishes.

### Detection bound

The bound `N + T` counts from the last frame received from the peer. The
reference node adds slack on top of it, so a Link closes a little later than the
bound, never earlier:

* the idle timer and the timeout timer run on the scheduler of the node, which
  adds scheduling delay to each;
* the best-effort `close` write (see [close notice](#close-notice)) waits up to
  its bound of 1 s before the transport closes, when the peer does not read.

### Early probes

`N` is the longest a node waits before it probes. The reference node probes
earlier, once, on each of these events. An early probe closes a dead Link within
`T`, and a healthy Link answers it and stays. Early probes requested while one
probe waits for its `pong` cause at most one more probe.

* **A new Link to the peer.** A node that adds a Link to a peer while it holds
  other Links to that peer sends one probe on each of those older Links at once,
  whatever their idle interval. A new Link often means the peer moved and an
  older Link is dead. A dead older Link closes within its `T`; a healthy one
  answers and stays.
* **A query deadline with no answer.** A query routed over the Link whose
  deadline passes with no `response` probes the Link once. A caller that cancels
  its query does not: only the deadline counts. A dead Link then closes within
  `T` of the deadline instead of within `N + T` of the last frame.
* **A removed local address.** When the node's own network addresses change and
  one is removed, the Links whose local endpoint holds a removed address are
  probed once, after a 500 ms wait that groups changes. A Link whose local
  endpoint is not an IP address, or is a wildcard address (the `kcp` listener
  reports one), never matches and keeps relying on its idle keepalive. An
  address that only appeared probes nothing.
* **The NAT keepalive.** A Link that the NAT traversal strategy punched is
  probed every 5 s during its first minute and every 15 s afterwards, to keep
  the NAT mapping open. This schedule is separate from `N`, and the more
  frequent of the two applies.

No other event probes early. A node may also send a probe in order to confirm a
Link live before it picks between duplicate Links to one peer; that probe joins
one already in flight.

### Write stall

A Link closes when one write stays blocked for `T`. A write blocks when the
transport takes no more bytes, because the peer stopped reading and the
transport's buffers are full. Each frame is one write, so the rule bounds one
frame, not the Link's throughput.

* A peer that leaves one write blocked for `T` is closed, so a reader slower
  than that loses the Link, as does a peer that never reads. A peer cannot keep
  a Link open by answering probes while it stops reading other frames.
* A peer observes this close as the transport ending. The node attempts a
  `close` with `Reason` `0` (`closed`), but the frame waits behind the stuck
  write, so the node closes the transport at the close notice bound (see
  [close notice](#close-notice)) and the frame is not delivered.
* The rule is separate from the ping timeout: the ping timeout starts when a
  probe is written and also covers that write, and the write stall rule covers
  every frame.

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
