# objects.read

Stream the bytes of an object. The operation has two modes:

* Without `out`, the response body is the object payload itself, with no
  astral framing.
* With `out`, the operation accepts the query and answers on a channel in that
  format: one `error_message`, or the payload as `bytes32` chunks ended by
  `eos`.

The caller must hold
[`mod.auth.see_objects_action`](../../auth/types/mod.auth.see_objects_action.md).
Without `out`, the query is rejected before any repository is opened when the
caller is not authorized, and a refused caller receives no bytes. With `out`,
the operation answers an `error_message` reading `not permitted` before any
repository is opened.

## Arguments

* id (object_id.sha256, required) – The id to read.
* offset (uint64) – Byte offset to start reading from. Defaults to 0.
* limit (uint64) – Maximum number of bytes to read. Defaults to 0 (no limit).
* repo (string8) – Repository to read from. Without it, the bytes come from the candidates the finders name.
* zone (zone) – Limits the query's routing zone and never widens it. Without it, the routing zone stands.
* out (string) – Output format of the framed mode (e.g. `bin`, `json`). Without it, the operation streams raw bytes.

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

A lookup of a `Partial Object ID` fails when a repository that stores objects
itself does not support lookup by `Hash`.

Without `out`, the operation rejects the query if the caller is not
authorized, the repository is missing, the read fails, or no candidate delivers
the object. A rejection carries no reason. On success the raw bytes of the
object are written directly to the response stream (no astral framing).

With `out`, the operation answers one of:

* An `error_message` reading `not permitted` if the caller is not authorized.
* An `error_message` reading `repository not found` if `repo` names no
  repository.
* An `error_message` reading `object not found` if no candidate delivers the
  object, or the read error's text if the read fails.
* The object's bytes as `bytes32` objects of at most 32768 bytes each, in
  order, followed by `eos`. Their concatenation is the payload of the raw mode.
  A failure after the first chunk ends the stream with an `error_message`
  instead of `eos`.

A candidate other than this node is always read in the raw mode.

## Examples

```shellsession
$ astral-query objects.read -id data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
hello world
```

```shellsession
$ astral-query objects.read -id data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa -offset 6 -limit 5
world
```

```shellsession
$ astral-query objects.read -id data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa -out json
{"Type":"bytes32","Object":"aGVsbG8gd29ybGQK"}
{"Type":"eos","Object":null}
```
