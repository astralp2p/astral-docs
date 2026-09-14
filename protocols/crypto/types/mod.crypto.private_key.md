# mod.crypto.private_key

A typed private key used by the node to derive public keys and produce signatures.

## Fields

* Type (string8) – Name of the key scheme (e.g. `secp256k1`).
* Key (bytes16) – Raw private-key bytes for the given scheme.

The text form is `<type>:<base64-encoded key>`; JSON encodes the object as its named
fields, not as that text. `Key` carries the same base64 in both forms.

## Example

```json
{
  "Type": "mod.crypto.private_key",
  "Object": {
    "Key": "Yt+8a1q4XbPnGZsbT5gV/Sj5y4kCmWNL2L4y3rXh0vQ=",
    "Type": "secp256k1"
  }
}
```
