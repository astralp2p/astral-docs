# mod.sys.register_manager_request

The registration an app sends to
[`sys.register_manager`](../ops/sys.register_manager.md) to become the
node's manager.

## Fields

* Name (string8) – The name the app gives itself. The node does not verify it.
* GrantPermits ([]mod.auth.permit) – Permits the app asks for, with their
  constraints. The node puts them in the same node→manager contract as
  `ContractPermits`; both lists mean the same.
* ContractPermits ([]mod.auth.permit) – The permits the app asks to hold in a
  signed node→manager contract, with their constraints.
* Policies ([]mod.sys.policy_binding) – Must be empty. A request with any
  [`mod.sys.policy_binding`](mod.sys.policy_binding.md) is refused: the
  admission policies are removed.

## Example

```json
{
  "Type": "mod.sys.register_manager_request",
  "Object": {
    "Name": "control-plane",
    "GrantPermits": [
      { "Action": "mod.user.see_swarm_action" }
    ],
    "ContractPermits": [],
    "Policies": []
  }
}
```
