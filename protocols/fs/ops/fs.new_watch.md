# fs.new_watch

Register a new watched filesystem repository that monitors a directory for changes and indexes its contents. The directory is scanned immediately in a background goroutine, the repository is added to the `objects.RepoLocal` group under the given name, and the label defaults to the name when omitted.

The caller must hold
[`mod.auth.admin_objects_action`](../../auth/types/mod.auth.admin_objects_action.md).
The query is rejected when the caller is not authorized. The user identity and
the node's own identity hold the action by default; a sibling node does not.

## Arguments

* path (string, required) – Absolute filesystem path to the directory to watch and index.
* name (string, required) – Name used to register the repository with the objects module.
* label (string) – Human-readable label for the repository. Defaults to the value of `name`.

## Returned objects

The operation returns one of:
* An `error_message` object if the watch repository cannot be created, repository registration fails, or the group assignment fails.
* An `ack` object on success.

## Examples

```shellsession
$ astral-query fs.new_watch -path /data/watched -name watched -out json
{"Type":"ack","Object":{}}
```
