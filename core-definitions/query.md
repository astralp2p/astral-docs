# Query

* A `Query` is used by [`Identities`](identity.md) to call each other's [`Operations`](op.md).
* A `Query` has a `Nonce`, `Caller` and `Target` identities, and a
  [`Query String`](query-string.md). Those four fields are the whole of the
  `Query` on the wire.
* A `Query` can be routed by various means: directly via [`Links`](link.md), relayed via
  [`Nodes`](node.md), as well as other means.
* A `Query` does not carry a [`Zone`](zone.md). A `Zone` is a property of the
  routing context at one [`Node`](node.md), not a field of the `Query`. It gates
  what that `Node` does with the query: forwarding to another `Node` requires
  the `Network` zone.
* A `Zone` reaches the wire only on the app-to-node hop, as a field of
  `mod.apphost.route_query_msg`. A `Node` that receives a `Query` over a
  [`Link`](link.md) routes it under a fresh context holding all three `Zones`.
  A `Zone` therefore constrains the forwarding decision of the `Node` that holds
  it; it does not travel with the `Query` and does not bound the distance the
  `Query` ultimately covers.
* The `Target` can reject the `Query` with a non-zero uint8 `Reject Code`.
* The generic and default `Reject Code` is 1. A `Reject Code` of 1 means a
  refusal and never a missing route. Other values are `Operation` specific.
* The reserved generic codes are:
  * `0` — accepted / success (not a rejection).
  * `1` — rejected (generic default).
  * `2` — invalid query.
  * `3` — canceled.
  * `4` — internal error.
  * `6` — timeout: the `Query` was not answered in time.
  * `7` — unavailable: the `Target` or the next hop could not be reached.
* `5` is not a generic code. A [`messaging`](../protocols/messaging/README.md)
  `Node` that predates the `not admitted` answer sends it when it does not admit
  a delivery.
* Values from 8 to 254 are `Operation` specific.
* `255` is link-private: a [`Link`](link.md) answer meaning "no route here"
  (see [`Link Multiplexer`](../topics/link-mux.md#response-semantics)). It is
  never a `Reject Code`. A `Node` sends a `Target`'s own 255 across a `Link` as
  1, and the receiving `Node` turns a link answer of 255 into route not found,
  so 255 never reaches a `Caller`.
* Routing produces `6` and `7` as well as a `Target`: a `Node` that cannot
  answer within its routing deadline or cannot reach the next hop rejects the
  `Query` with them (see [Routing outcomes](#routing-outcomes)).
* The `Target` can accept the `Query`, which begins a new [`Channel`](channel.md) between
  the `Caller` and the `Target`.

## Routing outcomes

* A routed `Query` ends in exactly one outcome. Each outcome has one cause.
* Accepted: a `Target` accepted the `Query`.
* Rejected with a `Reject Code`: a `Target` or a relaying `Node` refused the
  `Query`. A refusal is final: the same `Query` gets the same answer.
* Route not found: no `Node` on the path routes the `Query`. Causes are an
  unknown `Target`, and a `Node` that is reached but has no handler for the
  `Target` or the `Operation`.
* Unavailable, `Reject Code` 7: the route exists, but the next hop could not be
  reached. Causes are a `Link` write that failed, a `Link` that closed while the
  `Query` waited for its answer, a relay that could not be reached or proved the
  `Caller` to, a `Node` whose router is not ready, and a known `Node` to which
  no `Link` could be made.
* Timeout: no answer arrived within the routing deadline. A `Node` that relays
  the `Query` sends the timeout across a `Link` as `Reject Code` 6. The
  reference routing deadline is 60 s.
* Canceled: the `Caller` canceled the `Query` before an answer arrived.
* Target not allowed: a policy of the `Caller`'s `Node`, such as a directory
  filter, excludes the `Target`. A blocked `Query` never leaves the `Node`.
* A known `Node` is an `Identity` the `Node` holds an endpoint for. An
  `Identity` with no endpoint and no relay [`Contract`](contract.md) the `Node`
  holds is unknown, so a `Query` to it fails as route not found.
* A `Caller` retries unavailable and timeout with backoff; the reference
  backoff starts at 1 s and doubles up to 30 s. A `Caller` answers route not
  found by discovering the `Target` again or by stopping. A `Caller` stops on a
  refusal and on target not allowed.
* A known `Node` that never comes back answers unavailable on every attempt,
  so a `Caller` bounds its retries.
