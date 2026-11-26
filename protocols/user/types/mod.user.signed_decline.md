# mod.user.signed_decline

A [`mod.user.decline`](mod.user.decline.md) body paired with the issuer's
signature. It is the stored and propagated form of the answer, kept in the
`declines` directory of SwarmState.

[`user.answer_request`](../ops/user.answer_request.md) signs one and adds it to SwarmState. It is a [SwarmState entry](../README.md#swarmstate-entries).

## Fields

* Decline ([mod.user.decline](mod.user.decline.md)) – The embedded unsigned decline body.
* IssuerSig ([mod.crypto.signature](mod.crypto.signature.md)) – Signature produced with the issuer's private key over the decline body.

## Example

```json
{
  "Type": "mod.user.signed_decline",
  "Object": {
    "Decline": {
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
