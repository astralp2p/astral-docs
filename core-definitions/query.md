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
* The generic and default `Reject Code` is 1. Other values are `Operation`
  specific.
* The reserved generic codes are:
  * `0` — accepted / success (not a rejection).
  * `1` — rejected (generic default).
  * `2` — invalid query.
  * `3` — canceled.
  * `4` — internal error.
* Values above the reserved range are `Operation` specific.
* The `Target` can accept the `Query`, which begins a new [`Channel`](channel.md) between
  the `Caller` and the `Target`.
