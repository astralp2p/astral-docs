# mod.auth.register_signer_action

A [`mod.auth.action`](mod.auth.action.md) requesting permission for the actor to
claim one key on a [`crypto.register_signer`](../../crypto/ops/crypto.register_signer.md)
binding. The operation submits the action once for each distinct key.

The action grants no signature and no right to act as the key's identity. A
holder sees what is sent for signing under the keys it claims, and may refuse it.
The node verifies every signature a holder returns.

A permit for this action carries no constraints. A permit whose `Constraints`
bundle is non-empty is refused rather than granted in full.

No handler allows this action. The swarm root holds it: the user identity, or
the node's own identity while the node has no user, and a `privileged_member`
node ([auth, Authorization](../README.md#authorization)). Any other identity
holds it only through a contract chain the node has indexed, such as the contract an app's
host signs to carry out an Approval.
An app asks for it in the permits of
[`apphost.register`](../../apphost/ops/apphost.register.md) or with
[`apphost.request_contract`](../../apphost/ops/apphost.request_contract.md).

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
