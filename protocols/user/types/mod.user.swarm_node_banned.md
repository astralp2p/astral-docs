# mod.user.swarm_node_banned

Emitted by user when a valid expulsion of a node takes effect on this node. It travels as the `Data` of a [`mod.events.event`](../../events/types/mod.events.event.md) to the node's own receivers and never leaves the node.

The expulsion takes effect when this node issues it, receives it pushed, or reads it from SwarmState. The node need not be a member: a banned node outside the member set emits this event as well, and a banned member also emits [`mod.user.swarm_member_left`](mod.user.swarm_member_left.md). A receiver reads the current bans and does not trust the node the event names; the node closes its links to a banned node on it. A node emits the event once for each node.

## Fields

* NodeID (identity) – The node that the user banned.

## Example

```json
{
  "Type": "mod.user.swarm_node_banned",
  "Object": {
    "NodeID": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6"
  }
}
```
