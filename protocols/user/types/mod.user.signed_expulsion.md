# mod.user.signed_expulsion

A `mod.user.expulsion` body paired with the issuer's signature. `mod.user.signed_expulsion` is the wire, stored, and propagated form of a swarm ban.

## Fields

* Expulsion (mod.user.expulsion) – The embedded unsigned expulsion body.
* IssuerSig (mod.crypto.signature) – Signature produced with the issuer's private key over the expulsion body.

## Example

```json
{
  "Type": "mod.user.signed_expulsion",
  "Object": {
    "Expulsion": {
      "Issuer": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
      "Subject": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6",
      "ExpelledAt": "2026-06-19T10:00:00Z"
    },
    "IssuerSig": {
      "Data": "MEUCIQDg+5p9aT4q2QzVKbS9N5wXYrFh3vUaQ7E2lY0bX9pSAiB7H1k=",
      "Scheme": "asn1"
    }
  }
}
```
