# vfs.stat

Answer the entry at a path of a VFS.

The caller must hold [`mod.vfs.read_action`](../types/mod.vfs.read_action.md) for the VFS, unless the caller is the VFS identity, the node's user or the node. The operation answers an `error_message` reading `not permitted` before it looks up the VFS when the caller is not authorized.

## Arguments

* vfs (identity) – The VFS to read. Defaults to the caller.
* path (string, required) – The entry. The path `/` names the root.

## Returned objects

The operation returns one of:
* An `error_message` object reading `not permitted` if the caller is not authorized, `no such vfs` if the identity has no VFS, `invalid path` if `path` breaks the rules of a path, `not found` if no entry is at `path`, or `not a folder` if a parent in `path` names a file.
* A [`mod.vfs.entry`](../types/mod.vfs.entry.md) object for the entry. For `/` the entry has an empty `Name`, the folder flag, the `Object ID` of the root listing and the modification time of the root.

## Examples

```shellsession
$ astral-query vfs.stat -path /notes/a.txt -out json
{"Type":"mod.vfs.entry","Object":{"Flags":0,"ID":"data1csrtss41fiq9bbso9hftnd77uwo5su68na7xgueefbin7bdxpxod","ModTime":"2026-11-13T09:12:44.123456789Z","Name":"a.txt"}}
```
