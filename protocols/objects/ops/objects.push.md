# objects.push

Push objects to the node; each received object is offered to the registered receivers and an acceptance flag is returned per object.

## Arguments

* in (string8) – Input format.
* out (string8) – Output format.
* (stream) – A stream of arbitrary astral objects to push. Each object is capped at 32 KiB.

## Returned objects

The operation returns a stream of `bool` objects — one per pushed object — where `true` means a receiver accepted the object and `false` means it was rejected. An explicit `eos` input is answered with a final `eos`; a stream ended by EOF is not.

## Examples

```shellsession
$ echo '{"Type":"string8","Object":"hi"}' | astral-query objects.push -in json -out json
{"Type":"bool","Object":true}
```

```shellsession
$ echo '{"Type":"bool","Object":false}' | astral-query objects.push -in json -out json
{"Type":"bool","Object":false}
```
