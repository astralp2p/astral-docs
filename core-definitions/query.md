# Query

* A `Query` is used by [`Identities`](identity.md) to call each other's [`Operations`](op.md).
* A `Query` has a `Nonce`, `Caller` and `Target` identities, and a
  [`Query String`](query-string.md). Those four fields are the whole of the
  `Query` on the wire.
* A `Query` can be routed by various means: directly via [`Links`](link.md), relayed via
  [`Nodes`](node.md), as well as other means.
* A `Query` does not carry a [`Zone`](zone.md). A `Zone` scopes how far a query
  may be routed, but it belongs to the routing context rather than to the
  `Query`: on the wire it travels in the message that requests routing — for
  example `mod.apphost.route_query_msg` — and not in the `Query` itself.
  Reaching another `Node` still requires the `Network` zone.
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
