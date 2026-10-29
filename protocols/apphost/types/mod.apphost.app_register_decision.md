# mod.apphost.app_register_decision

An app register policy's answer to a
[`mod.apphost.app_register_request`](mod.apphost.app_register_request.md). A
delegate set by
[`apphost.set_app_register_policy`](../ops/apphost.set_app_register_policy.md)
writes one to its output stream.

## Fields

* Allow (bool) – `true` admits the registration. `false` refuses it, and the
  node ignores the other fields.
* GrantPermits ([]mod.auth.permit) – The permits the node records as
  node-local grants for the new identity.
* ContractPermits ([]mod.auth.permit) – The permits the node signs into a
  node→app contract for the new identity.
* Authorizers ([]mod.auth.authorizer_assignment) – Authorizer assignments the
  node records with the new identity as `Actor`. An entry that is null,
  invalid, or names an `Actor` refuses the registration.

The node writes exactly the permits listed, on the record each list names. A
policy may move a permit between the two lists or drop it.

## Example

```json
{
  "Type": "mod.apphost.app_register_decision",
  "Object": {
    "Allow": true,
    "GrantPermits": [
      { "Action": "mod.auth.serve_apps_action" },
      { "Action": "mod.auth.use_blueprints_action" }
    ],
    "ContractPermits": [
      { "Action": "mod.user.see_swarm_action" }
    ],
    "Authorizers": []
  }
}
```
