# mod.crypto.public_key

A typed public key used to verify signatures and identify signers.

## Fields

* Type (string8) – Name of the key scheme (e.g. `secp256k1`).
* Key (bytes16) – Raw public-key bytes for the given scheme.

The text form is `<type>:<hex-encoded key>`; JSON encodes the object as its named
fields, not as that text, and there `Key` is base64 rather than hex. A hex string
placed in `Key` is decoded as base64 and silently yields a different key.

## Example

```json
{
  "Type": "mod.crypto.public_key",
  "Object": {
    "Key": "Ar74hA6zXvKuPIPAfLV3kniQT5nLQQP3HjfMaZMa5eFf",
    "Type": "secp256k1"
  }
}
```
