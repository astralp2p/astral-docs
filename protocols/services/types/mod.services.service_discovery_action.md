# mod.services.service_discovery_action

A [`mod.auth.action`](../../auth/types/mod.auth.action.md) authorizing one
service on one contributing node.
[`services.discover`](../ops/services.discover.md) checks every requested
`(Service, NodeID)` pair before evaluating providers. Discovery grants no
permission to invoke offered operations.

The permit's `Constraints` bundle must contain exactly one
[`mod.services.discovery_scope`](mod.services.discovery_scope.md) that allows
the pair. Missing constraints, an empty bundle, multiple objects, or another
object type allow nothing.

The user has default permission for all services. Local swarm members have
default permission on other members, allowing them to carry app discoveries.
The hosting node checks the app's own scope first. The node has no default
grant for its own identity.

Other identities need a scoped node-local grant from
[`apphost.grant`](../../apphost/ops/apphost.grant.md) or a signed contract.

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.
* Service (string8) – The service to discover.
* NodeID (identity) – The node contributing the service.

In JSON the embedded action's fields appear directly in the `Object` value,
beside `Service` and `NodeID`, not under an `Action` key.

## Example

```json
{
  "Type": "mod.services.service_discovery_action",
  "Object": {
    "Nonce": "a1b2c3d4e5f60718",
    "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Service": "player",
    "NodeID": "02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f"
  }
}
```
