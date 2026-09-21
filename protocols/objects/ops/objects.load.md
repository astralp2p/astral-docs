# objects.load

Load a stored object (or a stream of objects) and decode it into its typed representation. Non-astral payloads are returned as `blob`.

The caller must hold
[`mod.auth.see_objects_action`](../../auth/types/mod.auth.see_objects_action.md).
The query is rejected before any repository is opened when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* id (object_id.sha256) – Id to load. If omitted, the operation streams ids from the input.
* repo (string8) – Repository to read from. Defaults to the read-default repository.
* zone (zone) – Zone filter for the read context. Defaults to all zones.
* unparsed (bool) – When true, raw bytes are passed through instead of being decoded into a typed object.
* out (string8) – Output format.
* (stream) – When `id` is omitted, a stream of `object_id.sha256` objects to load. An explicit `eos` input is answered with a final `eos`; a stream ended by EOF is not.

Each id, given as `id` or streamed, can be a
[`Partial Object ID`](../../../core-definitions/object-id.md). The lookup
matches it by `Hash` inside the selected repository. An id with a nonzero
`Size` matches only an object with that `Size` and that `Hash`.

## Returned objects

The operation returns one of:
* An `error_message` object if the repository is not found, the load fails, or an unexpected object is received on the input stream. A lookup of a `Partial Object ID` fails when a repository that stores objects itself does not support lookup by `Hash`.
* The decoded typed object for each id (one shot if `id` was given, otherwise one per streamed id). Non-astral payloads come back as `blob`.
* An `eos` object answering an explicit `eos` input.

## Examples

```shellsession
$ astral-query objects.load -id data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa -out json
{"Type":"string8","Object":"hello"}
```
