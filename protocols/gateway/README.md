# gateway

The `gateway` protocol lets nodes register themselves as reachable through a relay node and lets callers obtain raw connection sockets to those registered nodes. A registered node is described by a `mod.gateway.endpoint` that pairs a gateway identity with a target identity; a `mod.gateway.socket` carries the endpoint to dial plus a one-time nonce the recipient presents over the raw connection to claim its reserved slot.

Four ops manage the lifecycle of a gateway registration: `gateway.node_register` enrolls a node with a chosen visibility, `gateway.node_unregister` removes it, `gateway.node_list` streams the public registry, and `gateway.node_connect` issues a socket for the caller to reach a registered peer. `gateway.node_route` is used internally by the gateway to forward or accept inbound link connections.

Registration, connection reservation, and forwarding require [`mod.auth.use_gateway_action`](../auth/types/mod.auth.use_gateway_action.md). Every caller holds it while the gateway is enabled, and a disabled gateway refuses all three.

## Idle connections

A registered node keeps idle connections open to its gateway, so a caller can reach it without a routed link. Each idle connection follows this lifecycle:

1. The node calls `gateway.node_register` on the gateway and receives a `mod.gateway.socket` holding the gateway's endpoint and the registration nonce.
2. The node opens a raw exonet connection to the socket's `Endpoint` and sends the nonce as one framed `nonce64` object, in the default [`Channel`](../../core-definitions/channel.md#binary-encoding) framing: `String8("nonce64") ++ Bytes32(Payload)`. The gateway reads one framed object from every raw connection it accepts, and closes the connection unless that object is a nonce it knows. A registration nonce adds the connection to the registered node's idle set.
3. While the connection is idle, both sides exchange only gateway connection-control frames, in the same framing: [`mod.gateway.ping`](types/mod.gateway.ping.md), [`mod.gateway.handoff`](types/mod.gateway.handoff.md) and [`mod.gateway.handoff_ack`](types/mod.gateway.handoff_ack.md). Any other object closes the connection. A side sends a ping request once 30 seconds pass without a received frame and without a request of its own, and answers every request with a reply. A side closes an idle connection after 60 seconds without receiving any frame.
4. `gateway.node_connect` claims one idle connection of the named node and returns a `mod.gateway.socket` holding a fresh connector nonce to the caller. On claiming the connection the gateway sends `mod.gateway.handoff` on it. The registered node replies with `mod.gateway.handoff_ack`, and both sides leave idle mode: no more control frames flow, and the registered node accepts the connection as an inbound link.
5. The caller opens a raw exonet connection to the socket's `Endpoint` and sends the connector nonce, framed as in step 2. The gateway joins that connection to the claimed one and copies bytes in both directions, so the link handshake runs between the caller and the registered node. A claimed connection whose caller does not arrive within 30 seconds is closed.

The registered node opens idle connections until two are idle, and opens more whenever one of its gateway connections closes. When `gateway.node_connect` finds no idle connection for the named node, it returns an `error_message`.
