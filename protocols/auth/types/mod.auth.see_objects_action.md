# mod.auth.see_objects_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
read objects, object metadata, or the repository namespace. Every read operation
in the objects module submits this action before it acts, and rejects the query
when it is denied, before it opens a repository or accepts the connection. A
refused caller receives no bytes.

One action covers every read — `objects.read`, `objects.load`,
`objects.contains`, `objects.probe`, `objects.describe`, `objects.scan`,
`objects.search`, `objects.find` and `objects.repositories`. Reading bytes and
enumerating
ids are not separated: a caller that can enumerate a repository already holds
what guarding a single object would protect. Reading blueprints answers to
[`mod.auth.use_blueprints_action`](mod.auth.use_blueprints_action.md).

ObjectID and Repo declare the nouns the call touches. Neither is evaluated. An
operation that names no single object leaves ObjectID absent; one that names no
single repository leaves Repo empty.

A permit for this action carries no constraints. A permit whose `Constraints`
bundle is non-empty is refused rather than granted in full.

The user identity, the node's own identity and every node member of the node's
swarm hold this action by default, and nobody else. A node shows the objects in
its repositories to its swarm peers: a node that authorized its own caller asks
a peer as itself, and the peer trusts that decision. An app or any other
identity holds it through a node-local grant or a signed contract. A local
caller carrying no identity is routed as the node's own identity.

A node member of the node's swarm holds
[`mod.nodes.relay_for_action`](../../nodes/types/mod.nodes.relay_for_action.md)
for the user. A query it relays for the user reaches the node as the user.

## Fields

* Action ([`mod.auth.action`](mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.
* ObjectID (object_id.sha256, optional) – The object the call reads. Absent when the operation names no single object.
* Repo (string8) – The repository the call reads from. Empty when the operation names no single repository.

In JSON the embedded action's fields appear directly in the `Object` value,
beside `ObjectID` and `Repo`, not under an `Action` key.

## Example

```json
{
  "Type": "mod.auth.see_objects_action",
  "Object": {
    "Nonce": "a1b2c3d4e5f60718",
    "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "ObjectID": "data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "Repo": "main"
  }
}
```
