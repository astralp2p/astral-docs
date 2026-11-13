# mod.auth.see_objects_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
read objects, object metadata, or the repository namespace. Every read operation
in the objects module submits this action before it acts, and answers
`not permitted` when it is denied, before it opens a repository.
[`objects.read`](../../objects/ops/objects.read.md) streams raw bytes, so it
rejects the query instead.

One action covers every read — `objects.read`, `objects.load`,
`objects.contains`, `objects.probe`, `objects.describe`, `objects.scan`,
`objects.search`, `objects.find` and `objects.repositories`. Reading bytes and
enumerating ids are not separated: a caller that can enumerate a repository
already holds what guarding a single object would protect. Reading blueprints
answers to
[`mod.auth.use_blueprints_action`](mod.auth.use_blueprints_action.md).

ObjectID and Repo declare the nouns the call touches. An operation that names
no single object leaves ObjectID absent; one that names no single repository
leaves Repo empty. The handlers of the user module and of node-local grants
ignore both. The [`vfs`](../../vfs/README.md) module's handler evaluates ObjectID
and ignores Repo.

The `vfs` handler allows an action when all of these hold:

* The action names an ObjectID. An action without one is refused, so a batch
  form of [`objects.contains`](../../objects/ops/objects.contains.md),
  [`objects.probe`](../../objects/ops/objects.probe.md) and
  [`objects.load`](../../objects/ops/objects.load.md) that names no ObjectID
  stays refused.
* The ObjectID is complete. An ObjectID with a `Size` of 0 is refused, except the
  ObjectID of the empty content, `Size` 0 with the SHA-256 hash of no bytes.
* A file with that ObjectID is in a VFS that the actor may read: the actor is
  that VFS identity, or is allowed
  [`mod.vfs.read_action`](../../vfs/types/mod.vfs.read_action.md) for it, by a
  permit or by the VFS's [evaluator](../../vfs/README.md#evaluator) answering
  yes.

A database error refuses. A refusal looks the same for an unknown ObjectID and
for an ObjectID that belongs to another VFS. The handler is node-local: a VFS
identity cannot hand it on down a contract chain. It allows
[`objects.read`](../../objects/ops/objects.read.md),
[`objects.load`](../../objects/ops/objects.load.md),
[`objects.contains`](../../objects/ops/objects.contains.md) and
[`objects.probe`](../../objects/ops/objects.probe.md) of one file by ObjectID.
[`objects.describe`](../../objects/ops/objects.describe.md) and
[`objects.find`](../../objects/ops/objects.find.md) leave ObjectID absent, and
`objects.scan`, `objects.search` and `objects.repositories` name no object, so
the `vfs` handler allows none of the five. A caller that another handler allows,
such as an app with a node-local grant of this action, can still call them.

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
* ObjectID (object_id.sha256, optional) – The object the call reads. Absent when the operation names no single object, and in `objects.describe` and `objects.find`, which leave it absent although they take an id.
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
