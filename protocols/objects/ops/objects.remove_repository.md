# objects.remove_repository

Remove a repository by name. Built-in repositories cannot be removed.

The caller must hold
[`mod.auth.admin_objects_action`](../../auth/types/mod.auth.admin_objects_action.md).
The query is rejected before the repository is looked up when the caller is not
authorized.

## Arguments

* name (string8, required) – Name of the repository to remove.
* in (string8) – Input format.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object if the repository is not found or cannot be removed.
* An `ack` object once the repository is removed.

## Examples

```shellsession
$ astral-query objects.remove_repository -name scratch -out json
{"Type":"ack","Object":null}
```
