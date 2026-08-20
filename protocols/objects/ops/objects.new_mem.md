# objects.new_mem

Create a new in-memory repository and attach it to the `memory` repo group.

The caller must hold
[`mod.auth.store_objects_action`](../../auth/types/mod.auth.store_objects_action.md).
The query is rejected before any repository is opened when the caller is not
authorized.

## Arguments

* name (string8, required) – Name of the new repository.
* size (string8) – Maximum size (e.g. `64M`, `1G`). Defaults to the module-wide default memory size.
* in (string8) – Input format.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object if `size` cannot be parsed or the repository cannot be added (e.g. name already in use).
* An `ack` object once the repository is created and grouped.

## Examples

```shellsession
$ astral-query objects.new_mem -name scratch -size 16M -out json
{"Type":"ack","Object":null}
```
