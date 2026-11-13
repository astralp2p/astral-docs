# vfs.ls

List the entries of a folder of a VFS in ascending byte order of `Name`.

The caller must hold [`mod.vfs.read_action`](../types/mod.vfs.read_action.md) for the VFS, unless the caller is the VFS identity, the node's user or the node. The operation answers an `error_message` reading `not permitted` before it looks up the VFS when the caller is not authorized.

## Arguments

* vfs (identity) – The VFS to list. Defaults to the caller.
* path (string) – The folder to list. Defaults to `/`.

## Returned objects

The operation returns one of:
* An `error_message` object reading `not permitted` if the caller is not authorized, `no such vfs` if the identity has no VFS, `invalid path` if `path` breaks the rules of a path, `not found` if no entry is at `path`, or `not a folder` if `path`, or a parent in it, names a file. An `error_message` ends the stream and follows any entries already sent.
* A [`mod.vfs.entry`](../types/mod.vfs.entry.md) object for each entry of the folder. The `ID` of a folder entry is the `Object ID` of its [`mod.vfs.directory`](../types/mod.vfs.directory.md).
* An `eos` object terminating the stream.

## Examples

```shellsession
$ astral-query vfs.ls -path /notes -out json
{"Type":"mod.vfs.entry","Object":{"Flags":0,"ID":"data1csrtss41fiq9bbso9hftnd77uwo5su68na7xgueefbin7bdxpxod","ModTime":"2026-11-13T09:12:44.123456789Z","CreationTime":"2026-11-13T08:30:05.555555555Z","Name":"a.txt"}}
{"Type":"mod.vfs.entry","Object":{"Flags":1,"ID":"data1btxfr8wffpn5rcb9utccgibhbytcxc75qo4zb16nytpzfxrfybo1n","ModTime":"2026-11-13T09:10:02.987654321Z","CreationTime":"2026-11-13T08:30:05.555555555Z","Name":"drafts"}}
{"Type":"eos","Object":null}
```
