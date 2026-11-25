# mod.user.expel_action

A [`mod.auth.action`](../../auth/types/mod.auth.action.md) requesting permission
for the actor to expel Subject from the swarm. It is the one action a
`privileged_member` membership does not cover: only the user key expels.

No operation asks for this action yet; [`user.expel`](../ops/user.expel.md)
still asks for [`mod.user.admin_swarm_action`](mod.user.admin_swarm_action.md).

A permit carrying constraints is refused. This action evaluates no constraint.

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.
* Subject (identity) – Identity of the node to expel.

In JSON the embedded action's fields appear directly in the `Object` value,
not under an `Action` key.

## Example

```json
{
  "Type": "mod.user.expel_action",
  "Object": {
    "Nonce": "a1b2c3d4e5f60718",
    "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Subject": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6"
  }
}
```
