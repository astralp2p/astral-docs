# vfs.volumes

List the facts of every VFS of the node.

The caller must hold [`mod.vfs.manage_action`](../types/mod.vfs.manage_action.md), unless the caller is the node's user or the node. The operation answers an `error_message` reading `not permitted` to a query that arrived over a [`Link`](../../../core-definitions/link.md), whatever the caller holds, and to a caller that is not authorized.

## Arguments

This operation takes no arguments.

## Returned objects

The operation returns one of:
* An `error_message` object reading `not permitted` if the query comes from the network or the caller is not authorized. An `error_message` for a failed lookup ends the stream and follows any `mod.vfs.info` already sent.
* A [`mod.vfs.info`](../types/mod.vfs.info.md) object for each VFS, in the order the VFSes were created.
* An `eos` object terminating the stream.

## Examples

```shellsession
$ astral-query vfs.volumes -out json
{"Type":"mod.vfs.info","Object":{"Entries":1,"EntryLimit":1000000,"Quota":1073741824,"Root":"data1fysiashf4okmwa1g9o54m3h41m1i6xgjt39as4ws39q5hfyxuo8iq","Usage":6,"VFS":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"}}
{"Type":"eos","Object":null}
```
