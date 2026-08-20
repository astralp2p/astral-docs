# mod.auth.admin_objects_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
modify the node's repositories: which repositories it has, and what they hold.

The action gates every operation that destroys what the node holds or changes
which repositories it has — `objects.delete`, `objects.purge`,
`objects.remove_repository`, `fs.new_repo` and `fs.new_watch`.

Writing and destroying are separate authorities. Adding to a repository answers
to [`mod.auth.store_objects_action`](mod.auth.store_objects_action.md); an
issuer granting that does not thereby grant emptying the same repository.

Attaching a host filesystem directory makes every file under it an addressable
object, so `fs.new_repo` and `fs.new_watch` reach further than the repository
they name.

ObjectID, Repo and Path declare the nouns the call touches. None is evaluated.
Each is left unset by an operation that names no single object, repository, or
path.

A permit for this action carries no constraints. A permit whose `Constraints`
bundle is non-empty is refused rather than granted in full.

The user identity and the node's own identity hold this action by default, and
nobody else. It is narrower than
[`mod.auth.see_objects_action`](mod.auth.see_objects_action.md) and
[`mod.auth.store_objects_action`](mod.auth.store_objects_action.md), which the
whole local swarm holds: swarm membership is granted on request, so granting the
swarm here would leave a sibling free to attach a host directory. Widening it is
an operator's decision, not a default.

## Fields

* Action ([`mod.auth.action`](mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.
* ObjectID (object_id.sha256, optional) – The object the call modifies. Absent when the operation names no single object.
* Repo (string8) – The repository the call modifies. Empty when the operation names no single repository.
* Path (string8) – The filesystem path the call attaches. Empty when the operation names no path.

## Example

```json
{
  "Type": "mod.auth.admin_objects_action",
  "Object": {
    "Action": {
      "Nonce": "a1b2c3d4e5f60718",
      "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
    },
    "ObjectID": null,
    "Repo": "photos",
    "Path": "/srv/photos"
  }
}
```
