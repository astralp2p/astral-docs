# fs

The `fs` protocol integrates the local filesystem with the astral object graph. It registers filesystem directories as named object repositories and indexes the files they contain as addressable astral objects.

File locations are represented as `mod.fs.file_location` values pairing a node identity with a filesystem path. Filesystem watchers track directories for changes and emit `astrald.mod.fs.events.file_added`, `astrald.mod.fs.events.file_changed`, and `astrald.mod.fs.events.file_removed` events as the contents evolve.

Repositories are created with `fs.new_repo` and filesystem watchers are registered with `fs.new_watch`.

Both ops answer to
[`mod.auth.admin_objects_action`](../auth/types/mod.auth.admin_objects_action.md):
attaching a directory makes every file under it an addressable object, so the
grant reaches further than the repository it names. The user identity and the
node's own identity hold the action by default; a sibling node does not.
