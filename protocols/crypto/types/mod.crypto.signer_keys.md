# mod.crypto.signer_keys

The fixed key set of a [`crypto.register_signer`](../ops/crypto.register_signer.md)
binding. The app sends it once, as the first object on the channel. The set holds
1–64 distinct pairs.

A signer whose keys change closes the binding and opens another.

## Fields

* Keys ([]\*[`mod.crypto.signer_key`](mod.crypto.signer_key.md)) – The claimed pairs.

## Example

```json
{
  "Type": "mod.crypto.signer_keys",
  "Object": {
    "Keys": [
      {
        "Key": {
          "Key": "Anm+Zn753LusVaBilc6HCwcCm/zbLc4o2VnygVsW+BeY",
          "Type": "secp256k1"
        },
        "Scheme": "bip137"
      }
    ]
  }
}
```
