# mod.auth.admin_network_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
administer the node's network: read its network state, make it do network work,
and control its links and listeners.

The action gates 25 operations in three tiers. A holder of the action holds all
three tiers.

* Read network state – `nodes.links`, `nodes.sessions`,
  `nodes.resolve_endpoints`, `ip.local_addrs`, `ip.public_ip_candidates`,
  `ip.default_gateway`, `nat.list_holes`, `kcp.list_endpoint_local_mappings`
  and `nearby.list`.
* Initiate network work and consume holes – `nodes.new_link`, `nat.punch`,
  `nat.node_punch`, `nat.node_consume_hole`, `nearby.broadcast` and
  `services.sync`.
* Control links and listeners – `nodes.add_endpoint`, `nodes.close_link`,
  `nodes.migrate_session`, `tcp.new_ephemeral_listener`,
  `tcp.close_ephemeral_listener`, `kcp.new_ephemeral_listener`,
  `kcp.close_ephemeral_listener`, `kcp.set_endpoint_local_port`,
  `kcp.remove_endpoint_local_port` and `nat.set_enabled`.

Each of these operations submits the action with the query's caller as the
actor. The operation submits it before it reads network state, schedules work,
opens a socket, consumes a hole, or changes state. A refused caller receives a
rejection and no bytes.

The action answers permission only. The peer, session, hole, and endpoint checks
an operation makes stay in force for an authorized caller.

Using the node's public gateway answers to `mod.auth.use_gateway_action`, not to
this action.

## Holders

The node's own identity holds this action, including on an unclaimed node
before any swarm exists.

Every current node member of the node's swarm holds this action. A current node
member holds an unexpelled
[`mod.user.swarm_membership_action`](../../user/types/mod.user.swarm_membership_action.md)
contract from the node's user. A network link does not make a node a member. An app registration
does not make an identity a member.

The user identity holds this action, as it holds the other node-wide actions. A
user that adopts and expels swarm members already decides what the network is.

An app, or any other identity, holds it through one of two paths:

* A node-local grant – the node records a permit for the action against the
  identity. A grant is valid on the granting node alone and carries no portable
  evidence.
* A signed contract chain – a chain of `mod.auth.signed_contract`s, each
  carrying a permit for the action, from an identity that holds the action on
  the node down to the caller. Every link must be valid. Every link must carry
  the delegation the links below it use.

An app authorized through a grant, or through a contract the node issues,
remains the caller. The action names the app as its actor.

The NAT link strategy and session migration submit queries to the peer node as
the node's own identity: `nat.node_punch`, `nat.node_consume_hole`,
`kcp.new_ephemeral_listener`, `kcp.set_endpoint_local_port`,
`kcp.close_ephemeral_listener`, `kcp.remove_endpoint_local_port` and
`nodes.migrate_session`. The peer answers them when the node holds this action
on the peer: as a member of the peer's swarm, or through a grant or a contract
there.

A permit for this action carries no constraints. A permit whose `Constraints`
bundle is non-empty is refused rather than granted in full.

## Fields

* Action ([`mod.auth.action`](mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.

The action carries no field beyond the embedded base action.

## Example

```json
{
  "Type": "mod.auth.admin_network_action",
  "Object": {
    "Action": {
      "Nonce": "a1b2c3d4e5f60718",
      "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
    }
  }
}
```
