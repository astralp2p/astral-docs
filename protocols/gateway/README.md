# gateway

The `gateway` protocol lets nodes register themselves as reachable through a relay node and lets callers obtain raw connection sockets to those registered nodes. A registered node is described by a `mod.gateway.endpoint` that pairs a gateway identity with a target identity; a `mod.gateway.socket` carries the endpoint to dial plus a one-time nonce the recipient presents over the raw connection to claim its reserved slot.

Four ops manage the lifecycle of a gateway registration: `gateway.node_register` enrolls a node with a chosen visibility, `gateway.node_unregister` removes it, `gateway.node_list` streams the public registry, and `gateway.node_connect` issues a socket for the caller to reach a registered peer. `gateway.node_route` is used internally by the gateway to forward or accept inbound link connections.

Registration, connection reservation, and forwarding require [`mod.auth.use_gateway_action`](../auth/types/mod.auth.use_gateway_action.md). Every caller holds it while the gateway is enabled, and a disabled gateway refuses all three.
