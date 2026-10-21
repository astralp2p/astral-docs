# mod.user.swarm_invite_decision

A swarm invite policy's answer to a
[`mod.user.swarm_invite_request`](mod.user.swarm_invite_request.md). A delegate
set by [`user.set_swarm_invite_policy`](../ops/user.set_swarm_invite_policy.md)
writes one to its output stream.

## Fields

* Allow (bool) – `true` accepts the invitation, and the node signs the
  contract. `false` declines it.

## Example

```json
{
  "Type": "mod.user.swarm_invite_decision",
  "Object": {
    "Allow": true
  }
}
```
