# mod.auth.use_blueprints_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
read and register the node's [blueprints](../../../topics/blueprints.md).

One action covers every blueprint operation — `objects.blueprints`,
`objects.get_blueprint` and `objects.register_blueprint`. Each submits the
action with the query's caller as the actor and answers `not permitted` when
the action is denied, before it reads or registers a blueprint.

The action reads no object and writes no object.
[`mod.auth.see_objects_action`](mod.auth.see_objects_action.md) and
[`mod.auth.store_objects_action`](mod.auth.store_objects_action.md) do not cover
the blueprint operations.

A registered blueprint is node-wide: every caller decodes the type through it
from then on.

A permit for this action carries no constraints. A permit whose `Constraints`
bundle is non-empty is refused rather than granted in full.

The user identity and the node's own identity hold this action by default.
A `privileged_member` node of the node's swarm holds it through the swarm
root ([auth, Authorization](../README.md#authorization)). A node
member of another tier does not hold it under its own identity. An app, such a
node member, or any other identity holds it only
through a contract chain the node has indexed, such as the contract an app's
host signs to carry out an Approval. A local caller carrying no identity is routed as the node's own identity.

Every [`apphost.register`](../../apphost/ops/apphost.register.md) files a
contract request for this action for the new app. The app holds it once the
swarm approves the request.

## Fields

* Action ([`mod.auth.action`](mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.

In JSON the embedded action's fields appear directly in the `Object` value, not
under an `Action` key.

## Example

```json
{
  "Type": "mod.auth.use_blueprints_action",
  "Object": {
    "Nonce": "a1b2c3d4e5f60718",
    "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
  }
}
```
