# objects.echo

Echo received objects back to the caller, optionally filtered by type. Useful for debugging the object pipeline.

The caller must hold
[`mod.auth.store_objects_action`](../../auth/types/mod.auth.store_objects_action.md).
The query is rejected before any repository is opened when the caller is not
authorized.

## Arguments

* only (string8) – Comma-separated list of object types to echo. Other types are dropped.
* except (string8) – Comma-separated list of object types to drop. Other types are echoed.
* stop (string8) – Closes the channel when an object of this type is received (acts as an explicit terminator).
* strict (bool) – If true, an object whose blueprint is not registered causes an `error_message` and closes the stream; if false, unrecognized objects are silently skipped. Defaults to false.
* in (string8) – Input format.
* out (string8) – Output format.
* (stream) – Any objects to be echoed back. Unknown object types are silently skipped unless `strict` is set.

## Returned objects

The operation returns a stream of the same objects it received (subject to the `only`/`except` filters). The stream ends when the input closes or a `stop`-typed object arrives.

## Examples

```shellsession
$ echo '{"Type":"string8","Object":"ping"}' | astral-query objects.echo -in json -out json
{"Type":"string8","Object":"ping"}
```

```shellsession
$ echo '{"Type":"bool","Object":true}' | astral-query objects.echo -only bool -in json -out json
{"Type":"bool","Object":true}
```
