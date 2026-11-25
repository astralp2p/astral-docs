# mod.sys.policy_binding

One policy a manager decides, in a
[`mod.sys.register_manager_request`](mod.sys.register_manager_request.md).
[`sys.register_manager`](../ops/sys.register_manager.md) stores each
binding as the policy's delegate, with the manager as `identity`.

## Fields

* Policy (string8) – The policy: `app_register`, `grant_request`,
  `swarm_join`, `swarm_invite` or `contract_accept`. They decide
  [`apphost.register`](../../apphost/ops/apphost.register.md),
  `apphost.request_grant` (removed),
  `user.request_membership` (removed),
  `user.accept_membership` (removed) and
  [`user.accept_contract`](../../user/ops/user.accept_contract.md).
* Operation (string8) – The operation the node queries on the manager for each
  decision. Required.
* Timeout (duration) – How long the node waits for one answer. Zero waits 10
  minutes. A negative value or a value above 10 minutes is refused.

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
