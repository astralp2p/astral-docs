# mod.mcp.answer_agent_action

A [`mod.auth.action`](../../auth/types/mod.auth.action.md) requesting permission for the
actor to answer a [`Query`](../../../core-definitions/query.md) from another agent.

**The actor is the agent being called, not the caller.** Every action type names what its
actor does, and answering is the called agent's act. The distinction is not only a name:
the [`auth`](../../auth/README.md) protocol resolves an action it cannot grant directly by
walking the contracts the actor is subject to, so an action naming the caller as actor
would search the caller's delegations for a permission the called agent holds.

What the caller is permitted to reach is a separate action,
[`mod.mcp.call_agent_action`](mod.mcp.call_agent_action.md). A call between two agents
proceeds only when both are granted, and neither party's permission decides the other's.

The action is submitted where a call arrives — the router of the [`mcp`](../README.md)
protocol — before a parked `astral-listen` is claimed and before the query is queued. A
parked listener is not permission, and claiming one for a query about to be refused would
consume it. A denied query is answered `route_not_found`, as one addressed to an identity
the node holds no agent for is: a caller cannot tell an agent that refuses it from an
agent that does not exist.

Whether the action is granted is the [`auth`](../../auth/README.md) protocol's decision —
a registered handler, or an active
[`mod.auth.signed_contract`](../../auth/types/mod.auth.signed_contract.md) whose permits
include this action type. A node holding neither answers no call.

A permit for this action carries no constraints. A permit whose `Constraints` bundle is
non-empty is refused rather than granted in full.

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID. ActorID is the agent being called.
* FromID (identity) – The caller the actor is asking to answer.

## Example

```json
{
  "Type": "mod.mcp.answer_agent_action",
  "Object": {
    "Action": {
      "Nonce": "b2c3d4e5f6071829",
      "ActorID": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6"
    },
    "FromID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
  }
}
```
