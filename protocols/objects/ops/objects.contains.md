# objects.contains

Check whether a repository might contain an object method nature is probabilistic.

The caller must hold
[`mod.auth.see_objects_action`](../../auth/types/mod.auth.see_objects_action.md).
The query is rejected before any repository is opened when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* repo (string8, required) – Name of the repository to check.
* id (object_id.sha256) – The id to check for. If omitted, the operation streams ids from the input.
* in (string8) – Input format for streamed ids.
* out (string8) – Output format.
* (stream) – When `id` is omitted, a stream of `object_id.sha256` objects to check. An explicit `eos` input is answered with a final `eos`; a stream ended by EOF is not.

Each id, given as `id` or streamed, can be a
[`Partial Object ID`](../../../core-definitions/object-id.md). The lookup
matches it by `Hash` inside the selected repository. An id with a nonzero
`Size` matches only an object with that `Size` and that `Hash`.

## Returned objects

The operation returns one of:
* An `error_message` object if the repository is not found, the lookup fails, or an unexpected object is received on the input stream. A lookup of a `Partial Object ID` fails when a repository that stores objects itself does not support lookup by `Hash`.
* An `eos` object answering an explicit `eos` input.
* A `bool` object for each id (one shot if `id` was given, otherwise one per streamed id).

## Examples

```shellsession
$ astral-query objects.contains -repo local -id data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa -out json
{"Type":"bool","Object":true}
```
