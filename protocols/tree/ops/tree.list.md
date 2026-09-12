# tree.list

List the child keys at a path.

The caller must hold
[`mod.auth.see_node_state_action`](../../auth/types/mod.auth.see_node_state_action.md).
The query is rejected before any path is walked when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

* path (string8) – The path to list. Defaults to `/` if omitted.

## Returned objects

The operation returns a stream of `string8` objects, one per child key name, followed by an `eos` object.

## Examples

```shellsession
$ astral-query tree.list -path /mod -out json
{"Type":"string8","Object":"kcp"}
{"Type":"string8","Object":"log"}
{"Type":"string8","Object":"nat"}
{"Type":"string8","Object":"nearby"}
{"Type":"string8","Object":"tcp"}
{"Type":"string8","Object":"tor"}
{"Type":"string8","Object":"user"}
{"Type":"eos","Object":null}
```

```shellsession
$ astral-query tree.list -path /mod/tcp/settings -out json
{"Type":"string8","Object":"dial"}
{"Type":"string8","Object":"listen"}
{"Type":"eos","Object":null}
```
