# mod.auth.register_signer_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
claim one key on a [`crypto.register_signer`](../../crypto/ops/crypto.register_signer.md)
binding. The operation submits the action once for each distinct key.

The action grants no signature and no right to act as the key's identity. A
holder sees what is sent for signing under the keys it claims, and may refuse it.
The node verifies every signature a holder returns.

A permit for this action carries no constraints. A permit whose `Constraints`
bundle is non-empty is refused rather than granted in full.

Nobody holds this action by default. An identity holds it through a node-local
grant or a signed contract.
[`apphost.register`](../../apphost/ops/apphost.register.md) asks for a node-local
grant when `grant_permits` names the action. The node's register policy decides
whether the grant is written, and the default policy writes it.

## Fields

* Action ([`mod.auth.action`](mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.
* Key ([`mod.crypto.public_key`](../../crypto/types/mod.crypto.public_key.md)) – The key the actor claims.

In JSON the embedded action's fields appear directly in the `Object` value, not
under an `Action` key.

## Example

```json
{
  "Type": "mod.auth.register_signer_action",
  "Object": {
    "Nonce": "a1b2c3d4e5f60718",
    "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Key": {
      "Key": "Anm+Zn753LusVaBilc6HCwcCm/zbLc4o2VnygVsW+BeY",
      "Type": "secp256k1"
    }
  }
}
```
