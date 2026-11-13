# vfs.remove

Remove an entry of a VFS.

The caller must hold [`mod.vfs.write_action`](../types/mod.vfs.write_action.md) for the VFS, unless the caller is the VFS identity, the node's user or the node. The operation answers an `error_message` reading `not permitted` before it looks up the VFS when the caller is not authorized.

## Arguments

* vfs (identity) – The VFS to change. Defaults to the caller.
* path (string, required) – The entry to remove.
* recursive (bool) – When `true`, a folder is removed with everything below it. Defaults to `false`.

The folder that held the entry gets the node's time. The root cannot be removed. The content of a removed file stays in the repository until [`objects.purge`](../../objects/ops/objects.purge.md) deletes it, which it does only when no file of any VFS and no other holder holds it.

## Returned objects

The operation returns one of:
* An `error_message` object reading `not permitted` if the caller is not authorized, `no such vfs` if the identity has no VFS, `invalid path` if `path` breaks the rules of a path or names the root, `not found` if no entry is at `path`, `not a folder` if a parent in `path` names a file, or `folder not empty` if a folder has entries and `recursive` is not set.
* An `ack` object if the entry was removed.

## Examples

```shellsession
$ astral-query vfs.remove -path /notes -recursive true -out json
{"Type":"ack","Object":null}
```
