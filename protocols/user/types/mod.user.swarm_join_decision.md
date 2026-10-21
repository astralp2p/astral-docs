# mod.user.swarm_join_decision

A swarm join policy's answer to a
[`mod.user.swarm_join_request`](mod.user.swarm_join_request.md). A delegate set
by [`user.set_swarm_join_policy`](../ops/user.set_swarm_join_policy.md) writes
one to its output stream.

## Fields

* Allow (bool) – `true` admits the requester, and the node issues it a
  membership contract. `false` declines the request.

## Example

```json
{
  "Type": "mod.user.swarm_join_decision",
  "Object": {
    "Allow": true
  }
}
```
