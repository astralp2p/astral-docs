# mod.user.bootstrap_result

The reply of [`user.bootstrap`](../ops/user.bootstrap.md): the user that now
owns the node, the words that derive that user when the node generated them,
and an access token for that user.

## Fields

* Identity (identity) – The user, the issuer of the node's active contract.
* Mnemonic (string16) – The BIP-39 words the node generated, separated by
  single spaces. Empty when the caller sent the words.
* Token (string8) – An access token issued for the user, valid for 365 days.
  An [apphost](../../apphost/README.md) session that authenticates with it acts
  as the user.

## Example

```json
{
  "Type": "mod.user.bootstrap_result",
  "Object": {
    "Identity": "02a1...",
    "Mnemonic": "penalty stadium garlic ... rifle fitness garage",
    "Token": "b9c2e1a3d4f5867a"
  }
}
```
