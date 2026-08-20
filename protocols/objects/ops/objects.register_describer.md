# objects.register_describer

Register the caller as an external describer. The module proxies `objects.describe` calls back to the caller's identity for the lifetime of the registration. Network-originated queries are rejected.

The caller must hold
[`mod.auth.serve_objects_action`](../../auth/types/mod.auth.serve_objects_action.md)
for the `describer` role. The query is rejected when the caller is not
authorized.

## Arguments

* in (string8) – Input format.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object if the caller identity is missing/zero, the caller is the node itself, or the describer cannot be added.
* An `ack` object once the external describer is registered.

## Examples

```shellsession
$ astral-query objects.register_describer -out json
{"Type":"ack","Object":null}
```
