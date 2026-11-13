# vfs.statfs

Answer the facts about one VFS: its root, usage, inodes and limits.

The caller must hold [`mod.vfs.read_action`](../types/mod.vfs.read_action.md) for the VFS, unless the caller is the VFS identity, the node's user or the node. The operation answers an `error_message` reading `not permitted` before it looks up the VFS when the caller is not authorized.

## Arguments

* vfs (identity) – The VFS to describe. Defaults to the caller.

## Returned objects

The operation returns one of:
* An `error_message` object reading `not permitted` if the caller is not authorized, or `no such vfs` if the identity has no VFS.
* A [`mod.vfs.info`](../types/mod.vfs.info.md) object for the VFS.

## Examples

```shellsession
$ astral-query vfs.statfs -out json
{"Type":"mod.vfs.info","Object":{"InodeLimit":1000000,"Inodes":1,"Quota":1073741824,"Root":"data1fysiashf4okmwa1g9o54m3h41m1i6xgjt39as4ws39q5hfyxuo8iq","Usage":6,"VFS":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"}}
```
