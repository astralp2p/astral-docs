# gateway.node_route

Route a raw connection to a target identity. When the target is this node, the raw stream is accepted and an inbound link is established. When the target is another node, the connection is forwarded by recursively issuing `gateway.node_route` toward the target and piping both sides.

## Arguments

* target (identity, required) – Identity of the node to route the connection to.

## Returned objects

The operation accepts the raw query and transfers bytes bidirectionally. No typed objects are written to the response; the response stream is the routed connection payload.
