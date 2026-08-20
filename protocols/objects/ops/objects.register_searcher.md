# objects.register_searcher

Register the caller as an external searcher. The module proxies `objects.search` calls back to the caller's identity for the lifetime of the registration. Network-originated queries are rejected.

The caller must hold
[`mod.auth.serve_objects_action`](../../auth/types/mod.auth.serve_objects_action.md)
for the `searcher` role. The query is rejected when the caller is not
authorized.

## Arguments

* in (string8) – Input format.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object if the caller identity is missing/zero, the caller is the node itself, or the searcher cannot be added.
* An `ack` object once the external searcher is registered.

## Examples

```shellsession
$ astral-query objects.register_searcher -out json
{"Type":"ack","Object":null}
```
