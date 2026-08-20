# mod.auth.signed_contract

A `mod.auth.contract` co-signed by its issuer and subject. Both signatures
must verify against the corresponding identities before the auth module will
index the contract or consult it when authorizing actions.

## Fields

* Contract (mod.auth.contract) – The embedded contract being signed.
* IssuerSig (mod.crypto.signature) – Signature produced with the issuer's private key.
* SubjectSig (mod.crypto.signature) – Signature produced with the subject's private key.

Both signatures cover the same contract; each may use a different signature
scheme (e.g. `asn1` over the contract's object ID, or `bip137` over its
human-readable signable text).

## Example

```json
{
  "Type": "mod.auth.signed_contract",
  "Object": {
    "Issuer": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Subject": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6",
    "Permits": [
      { "Action": "mod.user.see_swarm_action" }
    ],
    "ExpiresAt": "2027-05-27T12:00:00+02:00",
    "IssuerSig": "asn1:MEUCIQDg+5p9aT4q2QzVKbS9N5wXYrFh3vUaQ7E2lY0bX9pSAiB7H1k=",
    "SubjectSig": "asn1:MEQCIA1k0kZl0ZTd5KQv0pZL5kE2c8R5Mz0qY1g6kPq3rTfMAiB7H1k="
  }
}
```
