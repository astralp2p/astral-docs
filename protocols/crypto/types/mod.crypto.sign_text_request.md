# mod.crypto.sign_text_request

A node's request on a [`crypto.register_signer`](../ops/crypto.register_signer.md)
binding to sign one text. The app replies with a
[`mod.crypto.sign_answer`](mod.crypto.sign_answer.md).

`RequestID` is random, nonzero, and never reused on the binding. It correlates
the answer and grants no permission.

## Fields

* RequestID (nonce64) – Correlation value the answer echoes.
* Key ([`mod.crypto.public_key`](mod.crypto.public_key.md)) – The claimed key to sign under.
* Scheme (string8) – The claimed scheme to sign with.
* Text (string16) – The text to sign.

## Example

```json
{
  "Type": "mod.crypto.sign_text_request",
  "Object": {
    "RequestID": "9f2c41aa07d3e815",
    "Key": {
      "Key": "Anm+Zn753LusVaBilc6HCwcCm/zbLc4o2VnygVsW+BeY",
      "Type": "secp256k1"
    },
    "Scheme": "bip137",
    "Text": "hello world"
  }
}
```
