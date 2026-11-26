# auth.list_authorizers

Stream every stored external authorizer assignment, then `eos`. A token value
is never sent: an assignment that carries one is sent with `TokenValue` empty,
and a token file or environment variable is sent by name
([`auth.set_authorizer`](auth.set_authorizer.md)).

The caller must hold
[`mod.auth.admin_manage_apps_action`](../types/mod.auth.admin_manage_apps_action.md);
answered `not permitted` otherwise.

## Arguments

* out (string, optional) – Output encoding format. Defaults to the channel
  default.

## Returned objects

The operation returns one of:
* An `error_message` reading `not permitted` if the caller is not authorized.
* Zero or more
  [`mod.auth.authorizer_assignment`](../types/mod.auth.authorizer_assignment.md)
  objects, followed by `eos`.

## Examples

```shellsession
$ astral-query auth.list_authorizers -out json
{"Type":"mod.auth.authorizer_assignment","Object":{"Action":"mod.messaging.send_action","Actor":null,"Endpoint":"astral://mailgate:mailgate.authorize","Timeout":0,"TokenFile":"","TokenEnv":"","TokenValue":""}}
{"Type":"eos","Object":""}
```
