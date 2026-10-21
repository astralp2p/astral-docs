# mod.user.swarm_join_request

The join request a swarm join policy decides. A delegate set by
[`user.set_swarm_join_policy`](../ops/user.set_swarm_join_policy.md) reads one
from its input stream for each
[`user.request_membership`](../ops/user.request_membership.md) call.

## Fields

* Requester (identity) – The node that asks to join the swarm: the caller of
  `user.request_membership`.

## Example

```json
{
  "Type": "mod.user.swarm_join_request",
  "Object": {
    "Requester": "037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590"
  }
}
```
