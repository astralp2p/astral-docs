# mod.sys.policy_binding

One entry of the `Policies` of a
[`mod.sys.register_manager_request`](mod.sys.register_manager_request.md). The
type stays on the wire only: policies are removed, and
[`sys.register_manager`](../ops/sys.register_manager.md) refuses a request that
holds any binding.

## Fields

* Policy (string8) – The name of a policy.
* Operation (string8) – An operation on the manager.
* Timeout (duration) – A wait for one answer.

## Example

```json
{
  "Type": "mod.sys.policy_binding",
  "Object": {
    "Policy": "swarm_join",
    "Operation": "cp.approve_join",
    "Timeout": 60000000000
  }
}
```
