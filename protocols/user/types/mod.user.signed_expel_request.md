# mod.user.signed_expel_request

A [`mod.user.expel_request`](mod.user.expel_request.md) body paired with the
filer's signature. It is the stored and propagated form of an expel request,
kept in the `requests` directory of SwarmState.

No operation files one yet. [`user.swarm_requests`](../ops/user.swarm_requests.md) streams one stored in SwarmState, and [`user.answer_request`](../ops/user.answer_request.md) answers it. It is a [SwarmState entry](../README.md#swarmstate-entries).

## Fields

* ExpelRequest ([mod.user.expel_request](mod.user.expel_request.md)) – The embedded unsigned request body.
* FiledBySig ([mod.crypto.signature](mod.crypto.signature.md)) – Signature produced with FiledBy's private key over the request body.

## Example

```json
{
  "Type": "mod.user.signed_expel_request",
  "Object": {
    "ExpelRequest": {
      "FiledBy": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
      "Subject": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6",
      "FiledAt": "2026-11-25T10:00:00Z",
      "Timeout": "2026-11-25T11:00:00Z"
    },
    "FiledBySig": {
      "Data": "MEUCIQDg+5p9aT4q2QzVKbS9N5wXYrFh3vUaQ7E2lY0bX9pSAiB7H1k=",
      "Scheme": "asn1"
    }
  }
}
```
