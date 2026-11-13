# vfs.create

Create the VFS of an identity, with an empty root folder, the default limits and no evaluator.

The caller must hold [`mod.vfs.manage_action`](../types/mod.vfs.manage_action.md), unless the caller is the node's user or the node. The operation answers an `error_message` reading `not permitted` to a query that arrived over a [`Link`](../../../core-definitions/link.md), whatever the caller holds, and to a caller that is not authorized.

## Arguments

* vfs (identity, required) – The VFS identity. Any non-zero identity is accepted, the identity of the node included.

A VFS that exists succeeds and changes nothing, its evaluator included. The new VFS names no [evaluator](../README.md#evaluator); [`vfs.set_evaluator`](vfs.set_evaluator.md) sets one. The new VFS gets the limits from the `byte_limit` and `inode_limit` keys of the module configuration, `1073741824` bytes and `1000000` inodes by default. [`apphost.register`](../../apphost/ops/apphost.register.md) creates the VFS of the app it registers without this operation. A VFS for a keypair of its own is created by chaining operations: [`secp256k1.new`](../../secp256k1/ops/secp256k1.new.md) answers a private key, [`objects.store`](../../objects/ops/objects.store.md) stores it, the caller takes the identity of the key, and this operation creates the VFS of that identity.

## Returned objects

The operation returns one of:
* An `error_message` object reading `not permitted` if the query comes from the network, the caller is not authorized, or `vfs` is the zero identity.
* An `ack` object if the VFS exists.

## Examples

```shellsession
$ astral-query vfs.create -vfs 02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f -out json
{"Type":"ack","Object":null}
```
