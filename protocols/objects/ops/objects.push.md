# objects.push

Push objects to the node; each received object is offered to the registered receivers and an acceptance flag is returned per object.

The caller must hold
[`mod.auth.store_objects_action`](../../auth/types/mod.auth.store_objects_action.md).
The query is rejected before any repository is opened when the caller is not
authorized.

## Arguments

* in (string8) – Input format.
* out (string8) – Output format.
* (stream) – A stream of arbitrary astral objects to push. Each object is capped at 32 KiB.

## Returned objects

The operation returns one of:
* A `bool` object per pushed object, where `true` means a receiver accepted the object and `false` means it was rejected.
* An `error_message` object if an input cannot be decoded, or if an input is of a type the operation does not accept. A decode failure ends the operation; a wrong-typed input does not.
* An `eos` object answering an explicit `eos` input. A stream ended by EOF is not answered.

## Examples

```shellsession
$ echo '{"Type":"string8","Object":"hi"}' | astral-query objects.push -in json -out json
{"Type":"bool","Object":true}
```

```shellsession
$ echo '{"Type":"bool","Object":false}' | astral-query objects.push -in json -out json
{"Type":"bool","Object":false}
```
