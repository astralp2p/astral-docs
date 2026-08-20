# indexing.enable_repo

Enable or disable indexing for a named object repository. Pass `disable` to deactivate a previously enabled repo. The op returns `ErrRepositoryNotFound` if the repository name is not known to the objects module.

The caller must hold
[`mod.auth.store_objects_action`](../../auth/types/mod.auth.store_objects_action.md).
Indexing state is node-wide, so changing it answers to the same action that
guards writes in the [`objects`](../../objects/README.md) protocol. The query
is rejected when the caller is not authorized.

## Arguments

* repo (string, required) – Name of the object repository to enable or disable.
* disable (bool) – When true, disables the repository instead of enabling it. Defaults to false.

## Returned objects

The operation returns one of:
* An `error_message` object if the repository is not found or the operation fails.
* An `ack` object on success.

## Examples

```shellsession
$ astral-query indexing.enable_repo -repo myrepo -out json
{"Type":"ack","Object":{}}
```

```shellsession
$ astral-query indexing.enable_repo -repo myrepo -disable true -out json
{"Type":"ack","Object":{}}
```
