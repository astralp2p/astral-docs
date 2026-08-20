# objects.probe

Probe an object to determine its astral type, MIME type, host repository, and read latency.

The caller must hold
[`mod.auth.see_objects_action`](../../auth/types/mod.auth.see_objects_action.md).
The query is rejected before any repository is opened when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* id (object_id.sha256) – Id to probe. If omitted, the operation streams ids from the input.
* repo (string8) – Repository to probe in. Defaults to the read-default repository.
* in (string8) – Input format.
* out (string8) – Output format.
* (stream) – When `id` is omitted, a stream of `object_id.sha256` objects to probe. An explicit `eos` input is answered with a final `eos`; a stream ended by EOF is not.

## Returned objects

The operation returns one of:
* An `error_message` object if the repository is not found, the probe fails, or an unexpected object is received on the input stream.
* An `eos` object answering an explicit `eos` input.
* A `mod.objects.probe` object for each id (one shot if `id` was given, otherwise one per streamed id).

## Examples

```shellsession
$ astral-query objects.probe -id data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa -out json
{"Type":"mod.objects.probe","Object":{"Type":"string8","Repo":"local","Mime":"text/plain; charset=utf-8","Time":421000}}
```
