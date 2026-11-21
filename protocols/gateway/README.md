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

## Configuration

A node reads its gateway settings from `gateway.yaml`:

| Key | Default | Meaning |
| --- | --- | --- |
| `gateway.enabled` | `false` | The node serves as a gateway. |
| `gateway.networks` | None | Per network name, the gateway's socket listener: `port`, and an optional `endpoint` handed out in `mod.gateway.socket` instead of the node's public IP. |
| `visibility` | `private` | The visibility the node registers with at every gateway it names: `public` or `private`. |
| `gateways` | None | The gateways the node registers with, one entry per gateway. |

A `gateways` entry has two keys:

* `id` (identity) – The gateway's identity.
* `endpoints` (list of strings, optional) – The gateway's own link endpoints, each in the form `network:address`, such as `tcp:203.0.113.7:1791`. The node splits each string at its first colon.

```yaml
visibility: public
gateways:
  - id: 02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f
    endpoints:
      - tcp:203.0.113.7:1791
```

A `gateways` entry that is not a mapping with these keys, such as a bare identity, stops node startup. An entry without `id`, and a second entry with the same `id`, also stop node startup.

## Registering with a configured gateway

For each `gateways` entry the node does the following:

1. Once every module has loaded its dependencies, the node parses the entry's endpoints. An endpoint with an unknown network or an invalid address is logged and skipped. The node still registers with the gateway, which it then reaches only through endpoints it learned elsewhere.
2. The node stores each parsed endpoint for the gateway's identity with a TTL of 7 days (604800 seconds). Unlike a row that [`nodes.add_endpoint`](../nodes/ops/nodes.add_endpoint.md) writes, a first-hand pull of the gateway's endpoints can cap this row, as [Withdrawn endpoints](../nodes/README.md#withdrawn-endpoints) states; the node stores it again at the points below. A query to the gateway, `gateway.node_register` included, links to the gateway through these rows.
3. The node calls `gateway.node_register` with its `visibility`. A failed attempt is retried after 1 second, with the delay doubling up to 15 minutes. A new local network address restarts the delay at 1 second and retries at once.
4. A successful registration starts the idle connections. The registration is up from the `mod.gateway.socket` answer until the idle connections fail: three consecutive failed dials or connections the gateway closes before their first frame. The node then registers again from step 3.

The node stores the entry's endpoints again with a fresh TTL at these points:

* After every successful registration.
* Every 24 hours while the registration is up.
* Before every later registration attempt.

The rows for a configured gateway therefore do not expire while the node runs, whether the registration is up or not.

## Advertised gateway endpoints

While its registration with a gateway `G` is up, a node resolves its own identity, in [`nodes.resolve_endpoints`](../nodes/ops/nodes.resolve_endpoints.md), to the `mod.gateway.endpoint` `gw:<G>:<node>` among its other endpoints, with a TTL of 7 days (604800 seconds). A node without an up registration with `G` resolves no endpoint through `G`, whether or not `G` is configured.
