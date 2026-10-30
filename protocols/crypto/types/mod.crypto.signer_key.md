# mod.crypto.signer_key

One claim of a [`crypto.register_signer`](../ops/crypto.register_signer.md)
binding: a complete public key and one signature scheme. No value of either
field stands for more than one key or scheme.

## Fields

* Key ([`mod.crypto.public_key`](mod.crypto.public_key.md)) – The key the app signs for. A `secp256k1` key is 33 bytes in compressed form.
* Scheme (string8) – The signature scheme the app produces under the key (`bip137` or `asn1`).

## Example

```json
{
  "Type": "mod.crypto.signer_key",
  "Object": {
    "Key": {
      "Key": "Anm+Zn753LusVaBilc6HCwcCm/zbLc4o2VnygVsW+BeY",
      "Type": "secp256k1"
    },
    "Scheme": "bip137"
  }
}
```
