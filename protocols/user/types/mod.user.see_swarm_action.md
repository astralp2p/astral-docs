# mod.user.see_swarm_action

A [`mod.auth.action`](../../auth/types/mod.auth.action.md) requesting permission
for the actor to read what the swarm is: the active contract's metadata, the
sibling nodes and their link state, the bans the user has issued, and the asset
set together with its delta ledger. When evaluating the request the auth module
matches a permit to the action by object type.

One action gates every read op in the `user` protocol — `user.info`,
`user.assets`, `user.sync_assets`, `user.list_siblings`, `user.swarm_status`
and `user.list_expelled`. Between them they answer one question: who and what
belongs to this swarm.

A permit carrying constraints is refused. This action evaluates no constraint,
so honouring a narrowed permit would grant it in full.

This action replaces `mod.user.info_action`.

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.

This action carries no extra fields of its own beyond the embedded
`mod.auth.action`.

## Example

```json
{
  "Type": "mod.user.see_swarm_action",
  "Object": {
    "Action": {
      "Nonce": "a1b2c3d4e5f60718",
      "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
    }
  }
}
```
