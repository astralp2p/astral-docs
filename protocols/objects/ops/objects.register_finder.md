# objects.register_finder

Register the caller as an external finder. The module proxies `objects.find` calls back to the caller's identity for the lifetime of the registration. Network-originated queries are rejected.

The caller must hold
[`mod.auth.serve_objects_action`](../../auth/types/mod.auth.serve_objects_action.md)
for the `finder` role. The query is rejected when the caller is not authorized.

## Arguments

* in (string8) – Input format.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object if the caller identity is missing/zero, the caller is the node itself, or the finder cannot be added.
* An `ack` object once the external finder is registered.

## Examples

```shellsession
$ astral-query objects.register_finder -out json
{"Type":"ack","Object":null}
```
