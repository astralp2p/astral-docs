# mod.mcp.call_agent_action

A [`mod.auth.action`](../../auth/types/mod.auth.action.md) requesting permission for the
actor to start a [`Query`](../../../core-definitions/query.md) to another agent.

The actor is the calling agent, and the action asks what that agent is permitted to
reach. What the agent on the other side is permitted to answer is a separate action,
[`mod.mcp.answer_agent_action`](mod.mcp.answer_agent_action.md). A call between two
agents proceeds only when both are granted, and neither party's permission decides the
other's.

The action is submitted where a call starts — the `astral-query` tool of the
[`mcp`](../README.md) endpoint — before the query is built. A denied agent is answered as
it is for a target that resolves to no [`Identity`](../../../core-definitions/identity.md):
it learns that it cannot reach the target, and not whether the target exists.

Whether the action is granted is the [`auth`](../../auth/README.md) protocol's decision —
a registered handler, or an active
[`mod.auth.signed_contract`](../../auth/types/mod.auth.signed_contract.md) whose permits
include this action type. A node holding neither denies every call.

A permit for this action carries no constraints. A permit whose `Constraints` bundle is
non-empty is refused rather than granted in full.

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID. ActorID is the calling agent.
* ToID (identity) – The agent the actor is asking to call.

## Example

```json
{
  "Type": "mod.mcp.call_agent_action",
  "Object": {
    "Action": {
      "Nonce": "a1b2c3d4e5f60718",
      "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
    },
    "ToID": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6"
  }
}
```
