# vfs.read

Stream the raw bytes of a file of a VFS. Unlike most ops, the response body is the content itself rather than a stream of typed objects.

The caller must hold [`mod.vfs.read_action`](../types/mod.vfs.read_action.md) for the VFS, unless the caller is the VFS identity, the node's user or the node. The query is rejected before the VFS is looked up when the caller is not authorized, and a refused caller receives no bytes.

## Arguments

* vfs (identity) – The VFS to read. Defaults to the caller.
* path (string, required) – The file.
* offset (uint64) – Byte offset to start reading from. Defaults to 0.
* limit (uint64) – Maximum number of bytes to read. Defaults to 0, which reads to the end of the file.

The content comes from the `local` repository group of this node, in the device zone. The node asks no other node for it. An `offset` below the `Size` of the file starts the read at that byte, and an `offset` equal to the `Size` reads 0 bytes. A `limit` above the remaining byte count reads to the end of the file. A file with no content reads 0 bytes without a repository.

## Returned objects

The operation rejects the query with `Reject Code` `2` (invalid query), before it looks at the caller, if `path` is missing or `vfs`, `offset` or `limit` does not parse. It rejects the query with code `1` if the caller is not authorized, the identity has no VFS, `path` breaks the rules of a path, no entry is at `path`, a parent in `path` names a file, `path` names a folder, `offset` is above the `Size` of the file, or the content is missing from the repository. On success the raw bytes of the file are written directly to the response stream (no astral framing).

The operation has no `error_message`: every failure is a rejection, with the generic [`Reject Code`](../../../core-definitions/query.md) `1` except for an argument error, and it carries no reason. A caller that needs the reason of a failure uses [`vfs.stat`](vfs.stat.md), which answers with an `error_message`.

## Examples

```shellsession
$ astral-query vfs.read -path /notes/a.txt
hello
```

```shellsession
$ astral-query vfs.read -path /notes/a.txt -offset 1 -limit 3
ell
```
