# mod.user.mnemonic

The BIP-39 words of the node's user, stored by
[`user.bootstrap`](../ops/user.bootstrap.md) and answered by
[`user.mnemonic`](../ops/user.mnemonic.md). It holds no passphrase.

## Fields

* Words (string16) – The BIP-39 words, separated by whitespace.

## Example

```json
{
  "Type": "mod.user.mnemonic",
  "Object": {
    "Words": "penalty stadium garlic ... rifle fitness garage"
  }
}
```
