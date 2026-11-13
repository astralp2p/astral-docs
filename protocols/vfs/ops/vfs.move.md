# vfs.move

Move or rename an entry of a VFS.

The caller must hold [`mod.vfs.write_action`](../types/mod.vfs.write_action.md) for the VFS, unless the caller is the VFS identity, the node's user or the node. The operation answers an `error_message` reading `not permitted` before it looks up the VFS when the caller is not authorized.

## Arguments

* vfs (identity) – The VFS to change. Defaults to the caller.
* from (string, required) – The entry to move.
* to (string, required) – The new path of the entry.

The missing parent folders of `to` are created. The moved entry keeps its `ModTime`, and both parent folders get the node's time. The root cannot be moved, and nothing can be moved onto the root. A folder cannot be moved into itself or beneath itself.

## Returned objects

The operation returns one of:
* An `error_message` object reading `not permitted` if the caller is not authorized, `no such vfs` if the identity has no VFS, `invalid path` if `from` or `to` breaks the rules of a path, names the root, or a folder would move into itself or beneath itself, `not found` if no entry is at `from`, `not a folder` if a parent in `from` or `to` names a file, `already exists` if an entry is at `to`, or `too many entries` if the folders created for `to` would exceed the entry limit of the VFS.
* A [`mod.vfs.entry`](../types/mod.vfs.entry.md) object for the moved entry at its new path.

## Examples

```shellsession
$ astral-query vfs.move -from /notes/a.txt -to /archive/a.txt -out json
{"Type":"mod.vfs.entry","Object":{"Flags":0,"ID":"data1csrtss41fiq9bbso9hftnd77uwo5su68na7xgueefbin7bdxpxod","ModTime":"2026-11-13T09:12:44.123456789Z","Name":"a.txt"}}
```
