# events

The `events` namespace defines the envelope a node wraps around an event it
raises about its own state. A [`mod.events.event`](types/mod.events.event.md)
carries a fresh nonce, the node's identity, the time the event was raised, and
the event object itself as `Data`.

The node delivers each event in process to its own object receivers, with the
node's identity as the sender. It never sends an event to another node. A
receiver acts on an event only when the sender is the node itself, so an event
that arrives from another identity, through
[`objects.push`](../objects/ops/objects.push.md) or inside an
[`ether`](../ether/README.md) broadcast, has no effect.

These objects travel as the `Data` of a `mod.events.event`:

* [`mod.ip.events.network_address_changed`](../ip/types/mod.ip.events.network_address_changed.md)
* [`mod.nodes.new_observed_endpoint_event`](../nodes/types/mod.nodes.new_observed_endpoint_event.md)
* [`mod.nodes.link_created_event`](../nodes/types/mod.nodes.link_created_event.md)
* [`mod.nodes.link_closed_event`](../nodes/types/mod.nodes.link_closed_event.md)
* [`mod.nodes.link_pressure_event`](../nodes/types/mod.nodes.link_pressure_event.md)

The namespace exposes no operations.
