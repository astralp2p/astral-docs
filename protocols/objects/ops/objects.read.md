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
* repo (string8) – Repository to read from. Without it, the bytes come from the candidates the finders name.
* zone (zone) – Limits the query's routing zone and never widens it. Without it, the routing zone stands.

## Sources

With `repo`, the operation reads that repository only.

Without `repo`, the operation runs
[`objects.find`](objects.find.md)'s finders under the query's zone and treats
each identity they name as a candidate source:

* Each distinct candidate is tried once, as it arrives. Candidates are tried
  concurrently, and local and remote candidates have no priority between them.
* A candidate equal to this node is read from its read-default repository.
* Any other candidate receives an `objects.read` query from this node, as this
  node, with `zone=dv`. The node authorized its caller; the candidate trusts
  that decision.
* The first candidate to deliver bytes, or to end cleanly with none, supplies
  the read. Discovery and every other attempt are cancelled.
* A candidate that fails before any bytes reach the caller gives way to the
  other candidates. A failure after bytes reach the caller fails the read; no
  other candidate takes over.
* Discovery is bounded to 30 seconds. Each candidate has 15 seconds to deliver
  its first bytes.

The `network` zone permits remote candidates. With `zone=dv` the read stays on
this node.

A query arriving from another node runs without the `network` zone, so the node
answers from its own repositories and asks no further candidate.

The `id` can be a
[`Partial Object ID`](../../../core-definitions/object-id.md). The lookup
matches it by `Hash` inside the selected repository, or inside each candidate's
repository. An `id` with a nonzero
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

The operation rejects the query if the caller is not authorized, the repository is missing, the read fails, or no candidate delivers the object. A lookup of a `Partial Object ID` fails when a repository that stores objects itself does not support lookup by `Hash`. On success the raw bytes of the object are written directly to the response stream (no astral framing).

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
