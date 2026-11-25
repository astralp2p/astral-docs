# mod.user.trusted_action

The tier permit of a [`trusted`](mod.user.tier.md) membership. A membership is a
[`mod.auth.contract`](../../auth/types/mod.auth.contract.md) that carries
exactly one tier permit ([Memberships](../README.md#memberships)). In the
contract's signable text the permit shows as the word `trusted`.

A permit carrying constraints is refused. This action evaluates no constraint.

No operation asks for this action yet.

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID.

This action carries no extra fields of its own beyond the embedded
`mod.auth.action`. In JSON the embedded action's fields appear directly in the
`Object` value, not under an `Action` key.

## Example

```json
{
  "Type": "mod.user.trusted_action",
  "Object": {
    "Nonce": "a1b2c3d4e5f60718",
    "ActorID": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6"
  }
}
```
