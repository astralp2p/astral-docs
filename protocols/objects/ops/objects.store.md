# objects.store

Encode typed astral objects and write them as new repository entries. The id of each stored object is returned.

The caller must hold
[`mod.auth.store_objects_action`](../../auth/types/mod.auth.store_objects_action.md).
The query is rejected before any repository is opened when the caller is not
authorized.

## Arguments

* repo (string8) – Repository to write into. Defaults to the write-default repository.
* in (string8) – Input format.
* out (string8) – Output format.
* (stream) – A stream of astral objects (typed or unparsed) to store. Each object is encoded and committed as a separate entry. An explicit `eos` input is answered with a final `eos`; a stream ended by EOF is not.

## Returned objects

The operation returns one of:
* An `error_message` object if the repository is not found or any store fails.
* An `object_id.sha256` object per successfully stored input object.
* An `eos` object answering an explicit `eos` input.

## Examples

```shellsession
$ echo '{"Type":"string8","Object":"hello"}' | astral-query objects.store -in json -out json
{"Type":"object_id.sha256","Object":"data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
```
