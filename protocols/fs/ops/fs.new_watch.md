# fs.new_watch

Register a new watched filesystem repository that monitors a directory for changes and indexes its contents. The directory is scanned immediately in a background goroutine, the repository is added to the `objects.RepoLocal` group under the given name, and the label defaults to the name when omitted.

The caller must hold
[`mod.auth.admin_objects_action`](../../auth/types/mod.auth.admin_objects_action.md).
The query is rejected when the caller is not authorized. The user identity and
the node's own identity hold the action by default; a sibling node does not.

Unless `temporary` is `true`, the repository is saved to the tree at `/mod/fs/repos/<name>` and registered again at the next node start. The entry holds the child nodes `path` (`string8`), `label` (`string8`) and `writable` (`bool`, `false`). [`objects.remove_repository`](../../objects/ops/objects.remove_repository.md) deletes the entry.

At node start, an entry is skipped when its name is already registered, or when its path is relative, missing or not a directory. A skipped entry stays in the tree. A `name` that is empty or contains `/` is rejected when the repository is saved.

## Arguments

* path (string, required) – Absolute filesystem path to the directory to watch and index.
* name (string, required) – Name used to register the repository with the objects module.
* label (string) – Human-readable label for the repository. Defaults to the value of `name`.
* temporary (bool) – When `true`, the repository is not saved to the tree and is gone after a node restart. Defaults to `false`.

## Returned objects

The operation returns one of:
* An `error_message` object if the watch repository cannot be created, repository registration fails, the group assignment fails, or the tree entry cannot be saved. A failed save removes the repository again.
* An `ack` object on success.

## Examples

```shellsession
$ astral-query fs.new_watch -path /data/watched -name watched -out json
{"Type":"ack","Object":{}}
$ astral-query fs.new_watch -path /tmp/scratch -name scratch -temporary true -out json
{"Type":"ack","Object":{}}
```
