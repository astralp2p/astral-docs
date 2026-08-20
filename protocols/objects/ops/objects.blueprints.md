# objects.blueprints

Stream every registered type name in dependency order: compile-time prototypes first, then runtime blueprints topologically sorted by reference. Each name is sent as a `string8` object; the stream is terminated by an `eos` object.

The caller must hold
[`mod.auth.see_objects_action`](../../auth/types/mod.auth.see_objects_action.md).
The query is rejected before any repository is opened when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object if sending a name fails.
* A stream of `string8` objects (one per registered type name) followed by an `eos` object.

## Examples

```shellsession
$ astral-query objects.blueprints -out json
{"Type":"string8","Object":"bool"}
{"Type":"string8","Object":"string8"}
{"Type":"string8","Object":"ack"}
{"Type":"string8","Object":"object_id.sha256"}
{"Type":"eos","Object":null}
```
