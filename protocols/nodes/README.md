# nodes

The `nodes` protocol manages encrypted links and multiplexed sessions between Astral nodes. It exposes operations for inspecting and managing links, resolving and registering known endpoints, and migrating sessions between links.

## Endpoint exchange in the local swarm

A node learns the endpoints of a member of its
[Local Swarm](../../core-definitions/local-swarm.md) by calling
[`nodes.resolve_endpoints`](ops/nodes.resolve_endpoints.md) on a linked member
and storing every returned endpoint with its TTL. A pull is a call of
`nodes.resolve_endpoints` on a member, the resolver, about a member, the
subject.

* When a new link is the node's only link to a member of its local swarm, the
  node pulls the endpoints of that member from that member.
* When a pushed membership contract reaches the node, the node pulls the
  endpoints of the contract's subject from the sender.
* When a node's own set of local addresses changes, the node announces the
  change to its linked members. A member that receives the announcement pulls
  the endpoints of the announcing node.

### Announcing a change

* A [`mod.ip.events.network_address_changed`](../ip/types/mod.ip.events.network_address_changed.md)
  event starts a 5 s wait, unless a wait is already running. A change during
  the wait joins that wait and starts no second one.
* An event whose `Added` and `Removed` hold only IPv6 link-local addresses
  starts no wait. A node never advertises an IPv6 link-local address.
* When the wait ends, the node pushes one
  [`mod.nodes.endpoints_changed_message`](types/mod.nodes.endpoints_changed_message.md)
  with `Subject` set to its own identity to every member of its local swarm it
  holds a link with. Each push is bounded to 15 s. A failed push is not retried.
* The message carries no endpoints. Endpoints travel only through
  `nodes.resolve_endpoints`, which requires
  [`mod.auth.admin_network_action`](../auth/types/mod.auth.admin_network_action.md).

### Receiving an announcement

A node accepts a pushed `mod.nodes.endpoints_changed_message` only when every
check passes:

* The sender is not the zero identity and is not the node itself.
* The node holds a link with the sender.
* The sender is a member of the node's local swarm.
* `Subject` is not the zero identity, is not the node itself, and is a member of
  the node's local swarm.

The node rejects any other `mod.nodes.endpoints_changed_message`, and the push
answers `false`. After accepting the message, the node:

1. Pulls the endpoints of `Subject` from the sender. The pull is bounded to 20 s.
   A failed pull is logged and not retried.
2. Counts the new rows. A row is new when the node held no unexpired endpoint of
   `Subject` with the same network and address before the pull. A row the pull
   refreshes is not new.
3. Emits a local
   [`mod.nodes.endpoints_updated_event`](types/mod.nodes.endpoints_updated_event.md)
   naming `Subject` when the pull stored at least one new row.
4. Forwards the message unchanged when the sender is `Subject`. The forward goes
   to every member of the node's local swarm the node holds a link with, except
   the sender and `Subject`, after the pull ends, with each push bounded to
   15 s. A message whose sender is not `Subject` is never forwarded, so a
   message travels at most one hop past the announcing node.

The [user](../user/README.md) module wakes the link to `Subject` on a
`mod.nodes.endpoints_updated_event`: a node that is not linked to `Subject`
dials at once instead of waiting out its backoff of up to 15 minutes.

An announcement withdraws no endpoint. An endpoint the announcing node no longer
holds stays stored until its TTL ends.
