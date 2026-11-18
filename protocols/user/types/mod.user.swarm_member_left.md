# mod.user.swarm_member_left

Emitted by user when a node leaves the node's [Local Swarm](../../../core-definitions/local-swarm.md) member set: the node is expelled, the node's last membership contract expires, or the active contract changes or is cleared. It travels as the `Data` of a [`mod.events.event`](../../events/types/mod.events.event.md) to the node's own receivers and never leaves the node.

The user module emits one `mod.user.swarm_member_left` per node gone from the set it last published, and nothing when the set is unchanged. When the last membership contract of a member node expires, the user module emits `mod.user.swarm_member_left` for that node one second after the contract's `ExpiresAt`. A member with several membership contracts leaves only when the latest of them expires. The expiry of the node's own membership contract triggers no comparison.

## Fields

* NodeID (identity) – The node that left.

## Example

```json
{
  "Type": "mod.user.swarm_member_left",
  "Object": {
    "NodeID": "035d6bfc7818844824354bd5ba1b7c08510139de14aa574e3f53a490814e3eab0e"
  }
}
```
