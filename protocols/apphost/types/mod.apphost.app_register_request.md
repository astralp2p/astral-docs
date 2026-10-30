# mod.apphost.app_register_request

The registration an app register policy decides. A delegate set by
[`apphost.set_app_register_policy`](../ops/apphost.set_app_register_policy.md)
reads one from its input stream for each
[`apphost.register`](../ops/apphost.register.md) call.

## Fields

* Origin (string8) – The caller's web origin. Empty for a local IPC caller.
* Name (string8) – The name the app gives itself. The node does not verify it.
* GrantPermits ([]mod.auth.permit) – The permits the app asks to hold as
  node-local grants. The list always begins with
  `mod.auth.serve_apps_action` and `mod.auth.use_blueprints_action`.
* ContractPermits ([]mod.auth.permit) – The permits the app asks to hold in a
  signed node→app contract.

## Example

```json
{
  "Type": "mod.apphost.app_register_request",
  "Object": {
    "Origin": "",
    "Name": "notes",
    "GrantPermits": [
      { "Action": "mod.auth.serve_apps_action" },
      { "Action": "mod.auth.use_blueprints_action" },
      { "Action": "mod.user.see_swarm_action" }
    ],
    "ContractPermits": []
  }
}
```
