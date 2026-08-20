# objects.get_type

Return the astral type name of an object, reading just enough bytes to parse the stamp and type header.

The caller must hold
[`mod.auth.see_objects_action`](../../auth/types/mod.auth.see_objects_action.md).
The query is rejected before any repository is opened when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* id (object_id.sha256, required) – The id to inspect.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object with `unknown type` if the object cannot be read, has no astral stamp, or the type cannot be parsed.
* A `string8` object containing the type name.

## Examples

```shellsession
$ astral-query objects.get_type -id data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa -out json
{"Type":"string8","Object":"string8"}
```
