# gateway.node_route

Route a raw connection to the named node. The node resolves `identity` before either branch runs, and rejects the query when `identity` does not resolve or resolves to the anonymous identity. When the named node is this node, the raw stream is accepted and an inbound link is established. Otherwise the connection is forwarded by recursively issuing `gateway.node_route` toward the named node, carrying the resolved identity in hex as `identity`, and piping both sides.

The two branches answer to different rules:

* Forwarding (the named node is another node) uses the gateway service. The caller must hold [`mod.auth.use_gateway_action`](../../auth/types/mod.auth.use_gateway_action.md), which every caller holds while the gateway is enabled. The query is rejected before the stream is accepted or any outbound query is routed when the gateway is disabled or the caller is not authorized, and a refused caller receives no bytes.
* Inbound (the named node is this node) is link admission. The link handshake authenticates the peer. The branch submits no action and does not require an enabled gateway.

## Arguments

* identity (string8, required) – Identity of the node to route the connection to, given as a hex public key or a name resolved via the directory.

## Returned objects

The operation rejects the query if `identity` does not resolve or resolves to the anonymous identity, and rejects a forwarding query if the gateway is disabled or the caller is not authorized. Otherwise it accepts the raw query and transfers bytes bidirectionally. No typed objects are written to the response; the response stream is the routed connection payload.
