# mod.user.derive_identity_result

The reply of [`user.derive_identity`](../ops/user.derive_identity.md): the user
that the words derive and, when the node generated them, the words.

## Fields

* Identity (identity) – The user the words derive along `m/1791'/0'/0'/0/0`,
  the user [`user.bootstrap`](../ops/user.bootstrap.md) claims the node for with
  the same words and passphrase.
* Mnemonic (string16) – The BIP-39 words the node generated, separated by
  single spaces. Empty when the caller sent the words.

## Example

```json
{
  "Type": "mod.user.derive_identity_result",
  "Object": {
    "Identity": "02a1...",
    "Mnemonic": "penalty stadium garlic ... rifle fitness garage"
  }
}
```
