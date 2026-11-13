# vfs.mkdir

Create a folder in a VFS, with its missing parent folders.

The caller must hold [`mod.vfs.write_action`](../types/mod.vfs.write_action.md) for the VFS, unless the caller is the VFS identity, the node's user or the node. The operation answers an `error_message` reading `not permitted` before it looks up the VFS when the caller is not authorized.

## Arguments

* vfs (identity) – The VFS to change. Defaults to the caller.
* path (string, required) – The folder to create.

A folder at `path` succeeds and changes nothing. The path `/` names the root, which always exists, and succeeds.

## Returned objects

The operation returns one of:
* An `error_message` object reading `not permitted` if the caller is not authorized, `no such vfs` if the identity has no VFS, `invalid path` if `path` breaks the rules of a path, `already exists` if a file is at `path`, `not a folder` if a parent in `path` names a file, or `no inodes left` if the folders would exceed the inode limit of the VFS.
* An `ack` object if the folder exists.

## Examples

```shellsession
$ astral-query vfs.mkdir -path /notes/drafts -out json
{"Type":"ack","Object":null}
```
