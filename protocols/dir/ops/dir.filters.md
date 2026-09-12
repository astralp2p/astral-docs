# dir.filters

Return the names of all registered identity filters. The op streams one `string8` per filter name and terminates with `eos`.

The caller must hold
[`mod.auth.see_node_state_action`](../../auth/types/mod.auth.see_node_state_action.md).
The query is rejected before any filter name is read when the caller is not
authorized, and a refused caller receives no bytes.

## Returned objects

The operation returns one of:
* A `string8` object for each registered filter name.
* An `eos` object terminating the stream.

## Examples

```shellsession
$ astral-query dir.filters -out json
{"Type":"string8","Object":"local"}
{"Type":"string8","Object":"friends"}
{"Type":"eos","Object":{}}
```
