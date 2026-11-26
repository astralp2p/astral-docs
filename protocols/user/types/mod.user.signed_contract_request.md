# mod.user.signed_contract_request

A [`mod.user.contract_request`](mod.user.contract_request.md) body paired with
the filer's signature. It is the stored and propagated form of a contract
request, kept in the `requests` directory of SwarmState.

[`apphost.register`](../../apphost/ops/apphost.register.md) and [`apphost.request_contract`](../../apphost/ops/apphost.request_contract.md) file one; [`user.swarm_requests`](../ops/user.swarm_requests.md) streams it and [`user.answer_request`](../ops/user.answer_request.md) answers it. It is a [SwarmState entry](../README.md#swarmstate-entries).

## Fields

* ContractRequest ([mod.user.contract_request](mod.user.contract_request.md)) – The embedded unsigned request body.
* FiledBySig ([mod.crypto.signature](mod.crypto.signature.md)) – Signature produced with FiledBy's private key over the request body.

## Example

```json
{
  "Type": "mod.user.signed_contract_request",
  "Object": {
    "ContractRequest": {
      "FiledBy": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
      "Identity": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6",
      "Permits": [
        { "Action": "mod.auth.serve_apps_action", "Constraints": null, "Delegation": 0 }
      ],
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
