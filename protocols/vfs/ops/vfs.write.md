# vfs.write

Create or replace a file of a VFS. The operation answers `ack` when its writer is open, receives the content as `blob` chunks until a `mod.objects.commit_msg`, commits the content to the default write repository, and answers the entry.

The caller must hold [`mod.vfs.write_action`](../types/mod.vfs.write_action.md) for the VFS, unless the caller is the VFS identity, the node's user or the node. The operation answers an `error_message` reading `not permitted` before it looks up the VFS and before it opens the writer when the caller is not authorized.

## Arguments

* vfs (identity) – The VFS to change. Defaults to the caller.
* path (string, required) – The file to create or replace.
* (stream) – `blob` objects holding the content, in order, then one [`mod.objects.commit_msg`](../../objects/types/mod.objects.commit_msg.md). A `blob` is an untyped object, so the `json` format cannot carry it. Send the stream in the `text` format, where a `blob` is `#[]:` followed by its Base64 payload.

The operation checks the VFS and the path before it opens the writer, so `is a folder` and `not a folder` arrive before the `ack`. The missing parent folders of `path` are created. A file at `path` is replaced, and a folder at `path` is refused. A commit message that follows no `blob` commits an empty file, which stores no object. The content goes to the group `local`, and the node never purges it while a file of any VFS holds its `Object ID`.

The stream is cut off when the received bytes exceed the bytes left under the byte limit of the VFS plus the size of the file being replaced. The operation then answers `quota exceeded`, discards the writer and commits nothing. After the commit the operation checks both limits against the VFS as it is, and a change that would grow the usage above a limit changes nothing. A stream that ends before the commit message changes nothing and receives no further answer. The content of a refused write stays in the repository, unheld, until a purge deletes it.

## Returned objects

The operation returns one of:
* An `error_message` object reading `not permitted` if the caller is not authorized, `no such vfs` if the identity has no VFS, `invalid path` if `path` breaks the rules of a path, `is a folder` if a folder is at `path`, `not a folder` if a parent in `path` names a file, `no storage` if the node has no writable repository, `quota exceeded` or `no inodes left` if the change would exceed a limit, `unexpected object: <type>` if the stream carries a decoded object other than `blob` or `mod.objects.commit_msg`, `stream corrupted: blueprint not found: <type>` if the stream carries an object whose type has no blueprint, or another error of the stream or of the writer if it fails. An `error_message` after the `ack` ends the operation, and the VFS is unchanged.
* An `ack` object acknowledging the open writer, then a [`mod.vfs.entry`](../types/mod.vfs.entry.md) object for the file after the commit. The entry has the node's time as `ModTime`.

## Examples

```shellsession
$ printf '%s\n%s\n' '#[]:aGVsbG8K' '#[mod.objects.commit_msg]' | astral-query vfs.write -path /notes/a.txt -in text -out json
{"Type":"ack","Object":null}
{"Type":"mod.vfs.entry","Object":{"Flags":0,"ID":"data1csrtss41fiq9bbso9hftnd77uwo5su68na7xgueefbin7bdxpxod","ModTime":"2026-11-13T09:12:44.123456789Z","Name":"a.txt"}}
```
