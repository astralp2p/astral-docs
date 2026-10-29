# mod.auth.use_gateway_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
use the node's public gateway service: register as a gateway-reachable node,
reserve a connection to a registered node, and forward a routed connection
through the node.

The action gates `gateway.node_register`, `gateway.node_connect`, and the
forwarding branch of `gateway.node_route`. Each refuses the query when the
gateway is disabled. Otherwise each submits the action with the query's caller
as the actor, and refuses the query when the action is denied. Both refusals
happen before any state changes. `gateway.node_register` and
`gateway.node_connect` answer an `error_message` reading `not permitted`.
`gateway.node_route` carries a raw stream, so it rejects the query and its
caller receives no bytes.

`gateway.node_route` addressed to the node itself is inbound-link admission, not
gateway use: it keeps its link handshake and submits no action.
`gateway.node_unregister` and `gateway.node_list` submit no action.

Every actor holds this action while the node's gateway is enabled
(`gateway.enabled` in the gateway module's config). No grant, contract, or swarm
membership is required. A disabled gateway refuses registration, reservation,
and forwarding even when a contract, a grant, or an external authority permits
the action.

Gateway use is service consumption, not network administration. Holding this
action grants nothing `mod.auth.admin_network_action` governs, and a gateway
client needs no `mod.auth.admin_network_action`.

A permit for this action carries no constraints. A permit whose `Constraints`
bundle is non-empty is refused rather than granted in full.

## Fields

* Action ([`mod.auth.action`](mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.

In JSON the embedded action's fields appear directly in the `Object` value, not
under an `Action` key.

## Example

```json
{
  "Type": "mod.auth.use_gateway_action",
  "Object": {
    "Nonce": "a1b2c3d4e5f60718",
    "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
  }
}
```
