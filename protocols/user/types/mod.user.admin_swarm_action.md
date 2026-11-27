# mod.user.admin_swarm_action

A [`mod.auth.action`](../../auth/types/mod.auth.action.md) requesting permission
for the actor to change what the swarm is: which nodes belong to it. When evaluating the request the auth module matches a permit
to the action by object type.

One action gates the swarm-administering ops in the `user` protocol:
`user.answer_request` and `user.introduce`. Two handlers decide it ([auth,
Authority in a swarm](../../auth/README.md#authority-in-a-swarm)). One allows the
actor when it is the user identity; it is not node-local, so a contract the user
signs may delegate the permit through the ordinary walk. The other allows a node
holding a `privileged_member` membership the user key issued; it is node-local,
so a Privileged member uses the action itself and no contract it signs passes
the action on.

Subject declares the noun a call touches. It is not evaluated. A
permit carrying constraints is refused, so honouring a narrowed permit would
grant it in full.

`user.expel` asks for [`mod.user.expel_action`](mod.user.expel_action.md)
instead, because expelling is the one action a `privileged_member` membership
does not cover.

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.
* Subject (identity) – Identity of the node introduced to, or the identity the answered request names.

In JSON the embedded action's fields appear directly in the `Object` value,
beside `Subject`, not under an `Action` key.

## Example

```json
{
  "Type": "mod.user.admin_swarm_action",
  "Object": {
    "Nonce": "a1b2c3d4e5f60718",
    "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Subject": "037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590"
  }
}
```
