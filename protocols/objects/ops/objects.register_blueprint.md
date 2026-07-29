# objects.register_blueprint

Register runtime `astral.blueprint` descriptors (struct kind or alias kind) with `DefaultBlueprints`. The op reads blueprints from the input stream until `eos` or EOF, registers each, and sends the resulting `object_id.sha256` or an `error_message` per input. An explicit `eos` input is answered with a final `eos`; a stream ended by EOF is not.

## Arguments

* in (string8) – Input format.
* out (string8) – Output format.
* (stream) – `astral.blueprint` objects to register, terminated by an `eos` object.

## Returned objects

The operation returns one of:
* An `error_message` object if a non-blueprint object is received or registration fails.
* An `object_id.sha256` object for each successfully registered blueprint.
* An `eos` object answering the input stream's `eos`.

## Examples

```shellsession
$ echo '{"Type":"astral.blueprint","Object":{"Fields":[{"Name":"Author","Spec":{"Type":"astral.blueprint.primitive_spec","Object":{"PrimitiveType":"identity"}}},{"Name":"Body","Spec":{"Type":"astral.blueprint.primitive_spec","Object":{"PrimitiveType":"string16"}}}],"Type":"example.message","Underlying":""}}
{"Type":"eos","Object":null}' | astral-query objects.register_blueprint -in json -out json
{"Type":"object_id.sha256","Object":"data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
{"Type":"eos","Object":null}
```

A `Field`'s `Spec` slot is interface-typed, so it is a nested "Type"/"Object" container — see [Blueprints § JSON](../../../topics/blueprints.md#json).
