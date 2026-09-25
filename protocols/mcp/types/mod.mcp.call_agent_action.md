# mod.mcp.call_agent_action

A [`mod.auth.action`](../../auth/types/mod.auth.action.md) requesting permission for the
actor to put a [`Query`](../../../core-definitions/query.md) to another identity through
the [`mcp`](../README.md) endpoint.

The actor is the calling agent, and the action asks what that agent is permitted to
reach. What the target does with a query that reaches it is the target's own decision,
and this action does not ask it.

The action guards the endpoint's generic queries: the `astral-query` tool and every
declared tool submit it before the query is built. A denied agent is answered as it is
for a target that resolves to no [`Identity`](../../../core-definitions/identity.md),
`unknown target`: it learns that it cannot reach the target, and not whether the target
exists.

Mail does not submit this action. The endpoint's mail tools call the
[`messaging`](../../messaging/README.md) module, which asks
[`mod.messaging.send_action`](../../messaging/types/mod.messaging.send_action.md) of the
sender and
[`mod.messaging.receive_action`](../../messaging/types/mod.messaging.receive_action.md)
of the recipient.

Whether the action is granted is the [`auth`](../../auth/README.md) protocol's decision —
a registered handler, or an active
[`mod.auth.signed_contract`](../../auth/types/mod.auth.signed_contract.md) whose permits
include this action type. A node holding neither denies every call.

A permit for this action carries no constraints. A permit whose `Constraints` bundle is
non-empty is refused rather than granted in full.

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID. ActorID is the calling agent.
* ToID (identity) – The target the actor is asking to query.

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
