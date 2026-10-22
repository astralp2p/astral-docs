# mod.user.bootstrap_result

The reply of [`user.bootstrap`](../ops/user.bootstrap.md): the user that now
owns the node and, when the node generated them, the words that derive that
user.

## Fields

* Identity (identity) – The user, the issuer of the node's active contract.
* Mnemonic (string16) – The BIP-39 words the node generated, separated by
  single spaces. Empty when the caller sent the words.

## Example

```json
{
  "Type": "mod.user.bootstrap_result",
  "Object": {
    "Identity": "02a1...",
    "Mnemonic": "penalty stadium garlic ... rifle fitness garage"
  }
}
```
