# mod.auth.authorizer_assignment

The external authorizer the node asks about one action type, after the swarm
root, its handlers and the contract chain have not allowed the action
([auth, Authorization](../README.md#authorization)).
[`auth.set_authorizer`](../ops/auth.set_authorizer.md) stores one, and
[`auth.list_authorizers`](../ops/auth.list_authorizers.md) streams them.

A zero `Actor` makes the assignment action-wide. An assignment with an `Actor`
answers for that actor alone and takes precedence over the action-wide one.

## Fields

* Action (string8) – The action's object type. Required.
* Actor (identity) – The actor the assignment answers for, or zero for every
  actor.
* Endpoint (string8) – The authorizer: `http://`, `https://` or `astral://`.
  Required.
* Timeout (duration) – How long the node waits for one answer. Zero takes the
  node's default.
* TokenFile (string8) – A file holding the bearer token of an `http` endpoint.
* TokenEnv (string8) – An environment variable holding it.
* TokenValue (string8) – The token itself. Never sent by
  `auth.list_authorizers`.

At most one of `TokenFile`, `TokenEnv` and `TokenValue` is set.

## The stored set

The node keeps its assignments as one `mod.auth.authorizer_assignments` value
in its tree at `/mod/auth/authorizers`, holding them in `Assignments`.

## Example

```json
{
  "Type": "mod.auth.authorizer_assignment",
  "Object": {
    "Action": "mod.messaging.send_action",
    "Actor": null,
    "Endpoint": "astral://mailgate:mailgate.authorize",
    "Timeout": 0,
    "TokenFile": "",
    "TokenEnv": "",
    "TokenValue": ""
  }
}
```
