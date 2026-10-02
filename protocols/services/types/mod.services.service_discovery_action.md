# mod.services.service_discovery_action

A [`mod.auth.action`](../../auth/types/mod.auth.action.md) requesting
permission for the actor to discover one service on one contributing node.
[`services.discover`](../ops/services.discover.md) submits one action per
requested service before it evaluates any provider.

Discovering a service grants nothing beyond learning its offering: every
operation the offering lists checks its own permission when it runs.

The action evaluates a permit's `Constraints` bundle. The bundle holds exactly
one [`mod.services.discovery_scope`](mod.services.discovery_scope.md), and the
permit covers the action when the scope allows its `Service` on its `NodeID`. A
permit with no constraints, an empty bundle, more than one object, or an object
of any other type covers nothing: discovery is always granted per service.

The user identity holds this action by default for every service. The node's
own identity holds none: a local caller that presents no identity acts as the
node, so a default for the node would reach every such caller. Any other
identity holds the action through a node-local grant with a scope, written by
[`apphost.grant`](../../apphost/ops/apphost.grant.md), or a signed contract.

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.
* Service (string8) – The service to discover.
* NodeID (identity) – The node contributing the service.

## Example

```json
{
  "Type": "mod.services.service_discovery_action",
  "Object": {
    "Action": {
      "Nonce": "a1b2c3d4e5f60718",
      "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
    },
    "Service": "player",
    "NodeID": "02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f"
  }
}
```
