# mod.coldcard.scan_action

A [`mod.auth.action`](../../auth/types/mod.auth.action.md) requesting permission
for the actor to scan the node's attached Coldcard devices: enumerate them,
request each device's derived public key, and refresh the node's device map.
When evaluating the request the auth module matches a permit to the action by
object type.

The action gates [`coldcard.scan`](../ops/coldcard.scan.md). The action grants
scanning alone. No signing or other device operation follows from it.

The user identity and the node's own identity hold this action by default, and
nobody else. Any other identity holds it through a node-local grant or a signed
[`mod.auth.contract`](../../auth/types/mod.auth.contract.md).

A permit carrying constraints is refused. This action evaluates no constraint,
so honouring a narrowed permit would grant it in full.

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.

This action carries no extra fields of its own beyond the embedded
`mod.auth.action`.

## Example

```json
{
  "Type": "mod.coldcard.scan_action",
  "Object": {
    "Action": {
      "Nonce": "a1b2c3d4e5f60718",
      "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
    }
  }
}
```
