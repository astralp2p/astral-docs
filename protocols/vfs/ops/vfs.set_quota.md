# vfs.set_quota

Set the byte limit and the entry limit of a VFS.

The caller must hold [`mod.vfs.manage_action`](../types/mod.vfs.manage_action.md), unless the caller is the node's user or the node. The operation answers an `error_message` reading `not permitted` to a query that arrived over a [`Link`](../../../core-definitions/link.md), whatever the caller holds, and to a caller that is not authorized.

## Arguments

* vfs (identity, required) – The VFS to change.
* bytes (uint64) – The byte limit. Defaults to 0, which means no limit.
* entries (uint64) – The entry limit. Defaults to 0, which means no limit.

The operation sets both limits, so an omitted argument removes that limit. A limit below the current usage is accepted. It refuses further growth and removes nothing. A limit above `9223372036854775807` is stored as `9223372036854775807`.

## Returned objects

The operation returns one of:
* An `error_message` object reading `not permitted` if the query comes from the network or the caller is not authorized, or `no such vfs` if the identity has no VFS.
* An `ack` object if the limits were set.

## Examples

```shellsession
$ astral-query vfs.set_quota -vfs 02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f -bytes 2147483648 -entries 5000 -out json
{"Type":"ack","Object":null}
```
