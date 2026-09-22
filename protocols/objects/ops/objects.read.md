# objects.read

Stream the raw bytes of an object. Unlike most ops, the response body is the object payload itself rather than a stream of typed objects.

The caller must hold
[`mod.auth.see_objects_action`](../../auth/types/mod.auth.see_objects_action.md).
The query is rejected before any repository is opened when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* id (object_id.sha256, required) – The id to read.
* offset (uint64) – Byte offset to start reading from. Defaults to 0.
* limit (uint64) – Maximum number of bytes to read. Defaults to 0 (no limit).
* repo (string8) – Repository to read from. Defaults to the read-default repository.
* zone (zone) – Zone filter for the read context. Defaults to all zones.

The `id` can be a
[`Partial Object ID`](../../../core-definitions/object-id.md). The lookup
matches it by `Hash` inside the selected repository. An `id` with a nonzero
`Size` matches only an object with that `Size` and that `Hash`.

`offset` and `limit` apply to the object the lookup matched, so a
`Partial Object ID` and the `Object ID` of the same object read the same bytes.
An `offset` below the object's `Size` starts the read at that byte, and an
`offset` equal to the object's `Size` reads 0 bytes. A `limit` of 0 reads from
`offset` to the end of the object, and a `limit` above the remaining byte count
reads to the end of the object.

A window is out of bounds when `offset` is above the object's `Size`, and when
`offset`, `limit` or the object's `Size` is above `9223372036854775807`. Each
of the three is carried as a `uint64` and compared as a signed 64-bit count. An
out-of-bounds window is a failed read.

## Returned objects

The operation rejects the query if the caller is not authorized, the repository is missing, or the read fails. A lookup of a `Partial Object ID` fails when a repository that stores objects itself does not support lookup by `Hash`. On success the raw bytes of the object are written directly to the response stream (no astral framing).

The operation has no `error_message`: every failure is a rejection, and it
carries no reason. A caller that needs the reason for a failed lookup uses
[`objects.load`](objects.load.md), which answers with an `error_message`.

## Examples

```shellsession
$ astral-query objects.read -id data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
hello world
```

```shellsession
$ astral-query objects.read -id data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa -offset 6 -limit 5
world
```
