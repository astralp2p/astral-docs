# mod.auth.sudo_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
act as another identity. The auth module's built-in handler allows this action
only when the actor and target are the same identity; granting it across
identities requires an active
[`mod.auth.signed_contract`](mod.auth.signed_contract.md) whose permits include
`mod.auth.sudo_action`.

The action gates every operation that takes one identity's authority for
another: the `as` argument of `shell.shell`, the `key` argument of
`crypto.sign_hash` and `crypto.sign_text`, and an apphost guest binding its
session to an identity.

An [`Identity`](../../../core-definitions/identity.md) is a public key, so
signing under another party's key is that party acting rather than a capability
of its own, and the signing operations name this action instead of one of their
own. A signature outlives the node's decision to produce it: it verifies on
every node for as long as the key lives, so a contract or grant signed under a
key the caller does not hold is genuine rather than merely accepted.

The node's own key is refused on the self branch. A local caller that presents no
identity is rewritten to the node's identity before an operation sees it, so
without the refusal an unauthenticated local caller would satisfy the actor-is-target
test and sign as the node. A caller holding a real sudo permit for the node still
signs, having proved something the rewrite cannot supply.

## Fields

* Action ([`mod.auth.action`](mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.
* AsID (identity) – Identity the actor is requesting to act as.

## Example

```json
{
  "Type": "mod.auth.sudo_action",
  "Object": {
    "Action": {
      "Nonce": "a1b2c3d4e5f60718",
      "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
    },
    "AsID": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6"
  }
}
```
