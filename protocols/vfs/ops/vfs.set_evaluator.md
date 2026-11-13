# vfs.set_evaluator

Set or clear the evaluator of a VFS: the endpoint the node asks about a read or a write that the built-in rules refuse. See [Evaluator](../README.md#evaluator).

The caller must be the VFS identity, the node's user or the node, or hold [`mod.vfs.manage_action`](../types/mod.vfs.manage_action.md). The operation answers an `error_message` reading `not permitted` to a query that arrived over a [`Link`](../../../core-definitions/link.md), whatever the caller is or holds, and to a caller that is not authorized.

## Arguments

* vfs (identity, required) – The VFS to change.
* endpoint (string8) – The evaluator, exactly `astral://<identity-or-alias>:vfs.authorize`, at most 255 bytes. Defaults to empty, which clears the evaluator.

The op of the endpoint is always `vfs.authorize`. The endpoint carries no query arguments (`?`), no caller part (`<caller>@`), and a non-empty identity or alias of the characters `a-z`, `A-Z`, `0-9`, `_`, `.` and `-`. The endpoint may name any identity, the VFS identity included. An endpoint of any other form, another op, `http://` and `https://` included, is refused and leaves the evaluator unchanged. The node checks the form again each time it asks, and refuses without a question when the stored endpoint is of another form. The node does not ask the evaluator when the field is set, so an evaluator that is not running is accepted. An alias in the endpoint is resolved each time the evaluator is asked. A VFS created with [`vfs.create`](vfs.create.md) or by [`apphost.register`](../../apphost/ops/apphost.register.md) with `Evaluator` false starts with an empty evaluator.

## Returned objects

The operation returns one of:
* An `error_message` object reading `not permitted` if the query comes from the network or the caller is not authorized, or `no such vfs` if the identity has no VFS.
* An `error_message` object reading `invalid endpoint` if the VFS exists and `endpoint` is not empty and is not `astral://<identity-or-alias>:vfs.authorize` of at most 255 bytes.
* An `ack` object if the evaluator was set or cleared.

## Examples

```shellsession
$ astral-query vfs.set_evaluator -vfs 02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f -endpoint astral://02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f:vfs.authorize -out json
{"Type":"ack","Object":null}
```

Clearing the evaluator:

```shellsession
$ astral-query vfs.set_evaluator -vfs 02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f -out json
{"Type":"ack","Object":null}
```
