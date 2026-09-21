# objects.delete

Delete an object (or a stream of objects) from a repository.

The caller must hold
[`mod.auth.admin_objects_action`](../../auth/types/mod.auth.admin_objects_action.md).
The query is rejected before the repository is looked up when the caller is not
authorized.

## Arguments

* repo (string8, required) – Repository to delete from. There is no default repository for delete.
* id (object_id.sha256) – Id to delete. If omitted, the operation streams ids from the input.
* zone (zone) – Zone filter for the delete context. Defaults to all zones.
* out (string8) – Output format.
* (stream) – When `id` is omitted, a stream of `object_id.sha256` objects to delete. An explicit `eos` input is answered with a final `eos`; a stream ended by EOF is not.

Each id, given as `id` or streamed, can be a
[`Partial Object ID`](../../../core-definitions/object-id.md). The lookup
matches it by `Hash` inside the selected repository. An id with a nonzero
`Size` matches only an object with that `Size` and that `Hash`.

## Returned objects

The operation returns one of:
* An `error_message` object if the repository is not found, the delete fails, or an unexpected object — including a stray `ack` — is received on the input stream. A lookup of a `Partial Object ID` fails when a repository that stores objects itself does not support lookup by `Hash`.
* An `eos` object answering an explicit `eos` input.
* An `ack` object for each successful delete (one shot if `id` was given, otherwise one per streamed id).

## Examples

```shellsession
$ astral-query objects.delete -repo local -id data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa -out json
{"Type":"ack","Object":null}
```
