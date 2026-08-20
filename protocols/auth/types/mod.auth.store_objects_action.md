# mod.auth.store_objects_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
write objects into the node: storing bytes, pushing objects at it, adding a
repository, registering a type, and turning indexing of a repository on or off.

One action covers every write that adds to node state — `objects.store`,
`objects.create`, `objects.push`, `objects.echo`, `objects.new_mem`,
`objects.register_blueprint`, `indexing.enable_repo` and `indexing.subscribe`.
Indexing state is node-wide: enabling a repository indexes every object in it
from then on, and a subscription consumes an indexer's change stream and
advances its cursor, so both are writes to node state.

This action does not cover deleting, purging, or removing a repository.

Repo and Type declare the nouns the call touches. Neither is evaluated. An
operation that names neither leaves both empty, as does an operation whose
subject arrives on the channel after the decision is made.

A permit for this action carries no constraints. A permit whose `Constraints`
bundle is non-empty is refused rather than granted in full.

The user identity and every node in the local swarm hold this action by default.

## Fields

* Action ([`mod.auth.action`](mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.
* Repo (string8) – The repository the call writes into. Empty when the operation names no single repository.
* Type (string8) – The object type the call writes. Empty when the operation names no single type.

## Example

```json
{
  "Type": "mod.auth.store_objects_action",
  "Object": {
    "Action": {
      "Nonce": "a1b2c3d4e5f60718",
      "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
    },
    "Repo": "main",
    "Type": ""
  }
}
```
