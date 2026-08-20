# objects.read

Stream the raw bytes of an object. Unlike most ops, the response body is the object payload itself rather than a stream of typed objects.

The caller must hold
[`mod.auth.see_objects_action`](../../auth/types/mod.auth.see_objects_action.md).
The query is rejected before any repository is opened when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* id (object_id.sha256, required) – The id to read.
* offset (uint64) – Byte offset to start reading from. Defaults to 0.
* limit (uint64) – Maximum number of bytes to read. Defaults to 0 (no limit).
* repo (string8) – Repository to read from. Defaults to the read-default repository.
* zone (zone) – Zone filter for the read context. Defaults to all zones.

## Returned objects

The operation rejects the query if the caller is not authorized, the repository is missing, or the read fails. On success the raw bytes of the object are written directly to the response stream (no astral framing).

## Examples

```shellsession
$ astral-query objects.read -id data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
hello world
```

```shellsession
$ astral-query objects.read -id data1aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa -offset 6 -limit 5
world
```
