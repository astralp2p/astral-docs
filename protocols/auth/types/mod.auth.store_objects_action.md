# mod.auth.store_objects_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
write objects into the node: storing bytes, adding a repository, turning
indexing of a repository on or off, and holding an object against purge.

One action covers every write that adds to node state — `objects.store`,
`objects.create`, `objects.echo`, `objects.new_mem`,
`indexing.enable_repo` and `apphost.hold_object`. A hold keeps an object from
`objects.purge`, so it is a write to node state. Registering a blueprint answers to
[`mod.auth.use_blueprints_action`](mod.auth.use_blueprints_action.md).
Indexing state is node-wide: enabling a repository indexes every object in it
from then on, so it is a write to node state.

This action does not cover `objects.push`. `objects.push` names no action, and
its receivers decide per object.

This action does not cover deleting, purging, or removing a repository. An
operation that destroys answers to
[`mod.auth.admin_objects_action`](mod.auth.admin_objects_action.md).

Repo and Type declare the nouns the call touches. Neither is evaluated. An
operation that names neither leaves both empty, as does an operation whose
subject arrives on the channel after the decision is made.

A permit for this action carries no constraints. A permit whose `Constraints`
bundle is non-empty is refused rather than granted in full.

The user identity and the node's own identity hold this action by default.
A `privileged_member` node of the node's swarm holds it through the swarm
root ([auth, Authorization](../README.md#authorization)). A node
member of another tier does not hold it under its own identity. An app, such a
node member, or any other identity holds it only
through a contract chain the node has indexed, such as the contract an app's
host signs to carry out an Approval. A local caller carrying no identity is routed as the node's own identity.

A `privileged_member` node holds
[`mod.nodes.relay_for_action`](../../nodes/types/mod.nodes.relay_for_action.md)
for the user, and no other node does. A query it relays for the user reaches
the node as the user.

## Fields

* Action ([`mod.auth.action`](mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.
* Repo (string8) – The repository the call writes into. Empty when the operation names no single repository.
* Type (string8) – The object type the call writes. Empty when the operation names no single type.

In JSON the embedded action's fields appear directly in the `Object` value,
beside `Repo` and `Type`, not under an `Action` key.

## Example

```json
{
  "Type": "mod.auth.store_objects_action",
  "Object": {
    "Nonce": "a1b2c3d4e5f60718",
    "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Repo": "main",
    "Type": ""
  }
}
```
