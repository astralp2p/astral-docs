# mod.user.swarm_member_joined

Emitted by user when a node enters the node's [Local Swarm](../../../core-definitions/local-swarm.md) member set. It travels as the `Data` of a [`mod.events.event`](../../events/types/mod.events.event.md) to the node's own receivers and never leaves the node.

The user module compares the member set after each change of membership contracts, expulsions or the active contract with the set it last published. It emits one `mod.user.swarm_member_joined` per node new to the set, and nothing when the set is unchanged. A node whose membership contract was in the index at startup emits no event.

## Fields

* NodeID (identity) – The node that joined.

## Example

```json
{
  "Type": "mod.user.swarm_member_joined",
  "Object": {
    "NodeID": "035d6bfc7818844824354bd5ba1b7c08510139de14aa574e3f53a490814e3eab0e"
  }
}
```
