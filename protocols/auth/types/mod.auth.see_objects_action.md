# mod.auth.see_objects_action

A `mod.auth.action` requesting permission for the actor to read objects,
object metadata, or the repository namespace. Every read operation in the
objects module submits this action before it acts, and rejects the query when
it is denied.

One action covers every read. Reading bytes and enumerating ids are not
separated: a caller that can enumerate a repository already holds what guarding
a single object would protect.

ObjectID and Repo declare the nouns the call touches. Nothing evaluates them.
An operation that names no single object leaves ObjectID absent; one that names
no single repository leaves Repo empty.

A permit for this action carries no constraints. A permit whose Constraints
bundle is non-empty is refused rather than granted in full.

## Fields

This action embeds `mod.auth.action` (Nonce, ActorID) and adds:

* ObjectID (object_id.sha256, optional) – The object the call reads. Absent when the operation names no single object.
* Repo (string8) – The repository the call reads from. Empty when the operation names no single repository.

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
