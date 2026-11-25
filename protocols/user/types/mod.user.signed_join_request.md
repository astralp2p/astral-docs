# mod.user.signed_join_request

A [`mod.user.join_request`](mod.user.join_request.md) body paired with the
joiner's signature. It is the stored and propagated form of a join request,
kept in the `requests` directory of SwarmState.

No operation stores, serves or accepts this type yet. It is a [SwarmState entry](../README.md#swarmstate-entries).

## Fields

* JoinRequest ([mod.user.join_request](mod.user.join_request.md)) – The embedded unsigned request body.
* JoinerSig ([mod.crypto.signature](mod.crypto.signature.md)) – Signature produced with the joiner's private key over the request body.

## Example

```json
{
  "Type": "mod.user.signed_join_request",
  "Object": {
    "JoinRequest": {
      "Joiner": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6",
      "Carrier": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
      "Tier": "member",
      "FiledAt": "2026-11-25T10:00:00Z",
      "Timeout": "2026-11-25T11:00:00Z"
    },
    "JoinerSig": {
      "Data": "MEUCIQDg+5p9aT4q2QzVKbS9N5wXYrFh3vUaQ7E2lY0bX9pSAiB7H1k=",
      "Scheme": "asn1"
    }
  }
}
```
