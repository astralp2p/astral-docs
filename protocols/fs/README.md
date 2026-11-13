# fs

The `fs` protocol integrates the local filesystem with the astral object graph. It registers filesystem directories as named object repositories and indexes the files they contain as addressable astral objects.

File locations are represented as `mod.fs.file_location` values pairing a node identity with a filesystem path. Filesystem watchers track directories for changes and update the repository's index as the contents evolve. The protocol declares the `astrald.mod.fs.events.file_added`, `astrald.mod.fs.events.file_changed`, and `astrald.mod.fs.events.file_removed` event types, but no node emits them: a watcher announces no change.

Repositories are created with `fs.new_repo` and filesystem watchers are registered with `fs.new_watch`.

A repository created by either op is saved to the tree under `/mod/fs/repos/<name>` and registered again at the next node start, unless the op receives `temporary` set to `true`.

Both ops answer to
[`mod.auth.admin_objects_action`](../auth/types/mod.auth.admin_objects_action.md):
attaching a directory makes every file under it an addressable object, so the
grant reaches further than the repository it names. The user identity and the
node's own identity hold the action by default; a sibling node does not.

## Writable repositories

A repository created by `fs.new_repo` is writable, as are the default repository and a configured or persisted repository whose entry has `writable` set to `true`. A repository created by `fs.new_watch` is read-only. A writable repository stores each object as one file directly in its directory. The file name is the text form of the object's `Object ID`.

A `Contains` check by a full `Object ID` answers `true` when the file exists, is a regular file, and has the size the `Object ID` names. A file of another size does not hold the object, so a truncated copy is not contained. A read opens the file under the same condition and otherwise fails with `object not found`. A check by a `Partial Object ID` resolves the object through the hash index.

A writer streams its bytes to a temp file named `.tmp.` followed by 16 hexadecimal characters, in the repository's directory, and a commit renames the temp file to the object's file name. A commit finds the object already stored when a regular file of that name exists and has the size of the `Object ID`. It then removes the temp file and keeps the stored file. A file of that name with another size is a truncated copy, and the rename replaces it. A commit of 0 bytes removes the temp file, stores nothing, and answers the `Object ID` of the empty content ([`objects.create`](../objects/ops/objects.create.md)).

A write that is interrupted before its commit or discard leaves its temp file in the directory. Registering a writable repository removes the temp files that the directory holds at that moment: the regular files directly in it whose names begin with `.tmp.`. The node lists them before the repository joins the objects module and removes them after the registration succeeds. A registration that fails removes nothing, and a writer opened after the registration keeps its temp file. A directory that does not exist has none to remove. A file that cannot be removed is logged and does not fail the registration. Registration happens in [`fs.new_repo`](ops/fs.new_repo.md) and, at node start, for the default repository, the repositories of the configuration file and the repositories persisted in the tree.

A writable repository claims its directory when it is registered. The claim resolves symbolic links, so two paths to one directory are one claim. A registration whose directory a registered writable repository already holds fails with an `error_message` reading `path <path> is the root of live repository <label>`, and the directory is left untouched. Removing the repository releases the claim.
