# vfs.touch

Set the modification time of an entry of a VFS.

The caller must hold [`mod.vfs.write_action`](../types/mod.vfs.write_action.md) for the VFS, unless the caller is the VFS identity, the node's user or the node. The operation answers an `error_message` reading `not permitted` before it looks up the VFS when the caller is not authorized.

## Arguments

* vfs (identity) – The VFS to change. Defaults to the caller.
* path (string, required) – The file or folder to touch.
* time (time) – The new modification time. Defaults to the node's time. A time before the Unix epoch, or outside the range the `time` type encodes, is refused.

The operation creates nothing. The root cannot be touched.

## Returned objects

The operation returns one of:
* An `error_message` object reading `not permitted` if the caller is not authorized, `no such vfs` if the identity has no VFS, `invalid path` if `path` breaks the rules of a path or names the root, `invalid time` if `time` cannot be encoded, `not found` if no entry is at `path`, or `not a folder` if a parent in `path` names a file.
* A [`mod.vfs.entry`](../types/mod.vfs.entry.md) object for the touched entry.

## Examples

```shellsession
$ astral-query vfs.touch -path /notes/a.txt -time 2026-01-01T00:00:00Z -out json
{"Type":"mod.vfs.entry","Object":{"Flags":0,"ID":"data1csrtss41fiq9bbso9hftnd77uwo5su68na7xgueefbin7bdxpxod","ModTime":"2026-01-01T00:00:00Z","Name":"a.txt"}}
```
