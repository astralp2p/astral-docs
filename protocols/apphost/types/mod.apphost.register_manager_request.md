# mod.apphost.register_manager_request

The registration an app sends to
[`apphost.register_manager`](../ops/apphost.register_manager.md) to become the
node's manager.

## Fields

* Name (string8) – The name the app gives itself. The node does not verify it.
* GrantPermits ([]mod.auth.permit) – The permits the app asks to hold as
  node-local grants, with their constraints.
* ContractPermits ([]mod.auth.permit) – The permits the app asks to hold in a
  signed node→app contract, with their constraints.
* Policies ([]mod.apphost.policy_binding) – The policies the manager decides,
  one [`mod.apphost.policy_binding`](mod.apphost.policy_binding.md) each.

## Example

```json
{
  "Type": "mod.apphost.register_manager_request",
  "Object": {
    "Name": "control-plane",
    "GrantPermits": [
      { "Action": "mod.user.see_swarm_action" }
    ],
    "ContractPermits": [],
    "Policies": [
      { "Policy": "app_register", "Operation": "cp.approve_app", "Timeout": 0 },
      { "Policy": "swarm_join", "Operation": "cp.approve_join", "Timeout": 60000000000 }
    ]
  }
}
```
