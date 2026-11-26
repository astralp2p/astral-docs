# mod.user.signed_approval

A [`mod.user.approval`](mod.user.approval.md) body paired with the issuer's
signature. It is the stored and propagated form of the answer, kept in the
`approvals` directory of SwarmState.

No operation stores, serves or accepts this type yet. It is a [SwarmState entry](../README.md#swarmstate-entries).

## Fields

* Approval ([mod.user.approval](mod.user.approval.md)) – The embedded unsigned approval body.
* IssuerSig ([mod.crypto.signature](mod.crypto.signature.md)) – Signature produced with the issuer's private key over the approval body.

## Example

```json
{
  "Type": "mod.user.signed_approval",
  "Object": {
    "Approval": {
      "Issuer": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
      "RequestID": "data1eotsgeey6k7os9bhn5c6aow7rqf7jqmayqyq87bwpfatmo7e8mdcp"
    },
    "IssuerSig": {
      "Data": "MEUCIQDg+5p9aT4q2QzVKbS9N5wXYrFh3vUaQ7E2lY0bX9pSAiB7H1k=",
      "Scheme": "asn1"
    }
  }
}
```
