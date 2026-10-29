# apphost.list_held_objects

List objects currently held by the calling app. Local-only — a query from the
network is answered `origin not allowed: network`.

## Arguments

This operation takes no arguments.

## Returned objects

The operation returns a stream of `object_id.sha256` objects, followed by an
`eos` object. If the caller has no identity, an `error_message` is returned
instead.

## Examples

```shellsession
$ astral-query apphost.list_held_objects -out json
{"Type":"object_id.sha256","Object":"3b1f5d8c0a9e2c6b41d7e9f0a8b2c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f80910"}
{"Type":"object_id.sha256","Object":"a8b2c1d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8091011223344556677889900aabb"}
{"Type":"eos","Object":null}
```
