# objects.probe

Probe an object to determine its astral type, MIME type, host repository, read latency, and `Object ID`.

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

Each id, given as `id` or streamed, can be a
[`Partial Object ID`](../../../core-definitions/object-id.md). The lookup
matches it by `Hash` inside the selected repository. An id with a nonzero
`Size` matches only an object with that `Size` and that `Hash`.

## Returned objects

The operation returns one of:
* An `error_message` object if the repository is not found, the probe fails, or an unexpected object is received on the input stream. A lookup of a `Partial Object ID` fails when a repository that stores objects itself does not support lookup by `Hash`.
* An `eos` object answering an explicit `eos` input.
* A `mod.objects.probe` object for each id (one shot if `id` was given, otherwise one per streamed id).

## Examples

```shellsession
$ astral-query objects.probe -id data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa -out json
{"Type":"mod.objects.probe","Object":{"Mime":"text/plain; charset=utf-8","ObjectID":"data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","Repo":"local","Time":421000,"Type":"string8"}}
```

Probing the untyped payload `hello` by its `Partial Object ID`:

```shellsession
$ astral-query objects.probe -id data0ym81js7f9cfdbauqoq3kash6f8o5naxfa878ejx8gbbuckjazgbr -out json
{"Type":"mod.objects.probe","Object":{"Mime":"text/plain; charset=utf-8","ObjectID":"data1km81js7f9cfdbauqoq3kash6f8o5naxfa878ejx8gbbuckjazgbr","Repo":"local","Time":421000,"Type":""}}
```
