# mod.user.admin_swarm_action

A [`mod.auth.action`](../../auth/types/mod.auth.action.md) requesting permission
for the actor to change what the swarm is: which nodes belong to it, and which
objects it carries. When evaluating the request the auth module matches a permit
to the action by object type.

One action gates every mutating op in the `user` protocol — `user.adopt`,
`user.expel`, `user.add_asset`, `user.remove_asset` and `user.sync_with`.
Membership and the asset set are one authority: both decide what the swarm
holds, and both propagate from this node to every sibling.

Subject and ObjectID declare the nouns a call touches. Neither is evaluated. A
permit carrying constraints is refused, so honouring a narrowed permit would
grant it in full.

This action replaces `mod.user.adopt_action` and `mod.user.expel_action`.

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.
* Subject (identity) – Identity of the node being adopted, expelled or synced with. Zero for an asset call.
* ObjectID (object_id) – ID of the asset being added or removed. Zero for a membership call.

## Example

```json
{
  "Type": "mod.user.admin_swarm_action",
  "Object": {
    "Action": {
      "Nonce": "a1b2c3d4e5f60718",
      "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
    },
    "Subject": "037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590",
    "ObjectID": ""
  }
}
```
