# mod.apphost.policy_binding

One policy a manager decides, in a
[`mod.apphost.register_manager_request`](mod.apphost.register_manager_request.md).
[`apphost.register_manager`](../ops/apphost.register_manager.md) stores each
binding as the policy's delegate, with the manager as `identity`.

## Fields

* Policy (string8) – The policy: `app_register`, `grant_request`,
  `swarm_join`, `swarm_invite` or `contract_accept`. They decide
  [`apphost.register`](../ops/apphost.register.md),
  [`apphost.request_grant`](../ops/apphost.request_grant.md),
  [`user.request_membership`](../../user/ops/user.request_membership.md),
  [`user.accept_membership`](../../user/ops/user.accept_membership.md) and
  [`user.accept_contract`](../../user/ops/user.accept_contract.md).
* Operation (string8) – The operation the node queries on the manager for each
  decision. Required.
* Timeout (duration) – How long the node waits for one answer. Zero waits 10
  minutes. A negative value or a value above 10 minutes is refused.

## Example

```json
{
  "Type": "mod.apphost.policy_binding",
  "Object": {
    "Policy": "swarm_join",
    "Operation": "cp.approve_join",
    "Timeout": 60000000000
  }
}
```
