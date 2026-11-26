# auth.remove_authorizer

Remove the external authorizer assignment of an action type, action-wide or
for one actor. Removing an actor's assignment makes the action-wide one apply
to that actor again. Removing an absent assignment succeeds. A start restores
an assignment the `external_authorizers` of `auth.yaml` names
([`auth.set_authorizer`](auth.set_authorizer.md)).

The caller must hold
[`mod.auth.admin_manage_apps_action`](../types/mod.auth.admin_manage_apps_action.md);
answered `not permitted` otherwise.

## Arguments

* action (string8, required) – The action's object type.
* actor (string8, optional) – The identity or alias of an actor's assignment.
  Absent removes the action-wide one.

## Returned objects

The operation returns one of:
* An `error_message` reading `not permitted` if the caller is not authorized.
* An `error_message` if `actor` does not resolve.
* An `error_message` if storing the change fails.
* An `ack` once the removal is stored.

## Examples

```shellsession
$ astral-query auth.remove_authorizer -action mod.messaging.send_action -out json
{"Type":"ack","Object":null}
```
