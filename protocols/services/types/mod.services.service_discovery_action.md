# mod.services.service_discovery_action

A [`mod.auth.action`](../../auth/types/mod.auth.action.md) authorizing one
service on one contributing node.
[`services.discover`](../ops/services.discover.md) shows a holder every
offering of the service on that node, private providers included. Without it,
a swarm caller sees only open providers and other callers see nothing; see
[Visibility](../ops/services.discover.md#visibility). Discovery grants no
permission to invoke offered operations.

The permit's `Constraints` bundle must contain exactly one
[`mod.services.discovery_scope`](mod.services.discovery_scope.md) that allows
the pair. Missing constraints, an empty bundle, multiple objects, or another
object type allow nothing.

The user holds the action for all services, and so does a `privileged_member`
node through the swarm root. No other identity holds it by default, and the
node's own identity does not hold it. A member that carries an app's discovery
to another member does so under
[`mod.nodes.relay_for_action`](../../nodes/types/mod.nodes.relay_for_action.md)
for the app, and the hosting node checks the app's own scope when it filters
the members' results.

Other identities need a scoped permit in a signed contract. An app asks for
one with [`apphost.register`](../../apphost/ops/apphost.register.md) or
[`apphost.request_contract`](../../apphost/ops/apphost.request_contract.md),
which file a contract request in SwarmState; the app's host signs the contract
once the swarm approves the request. Contracts for different services add
up.

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
