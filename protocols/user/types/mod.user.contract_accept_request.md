# mod.user.contract_accept_request

The contract a contract accept policy decides. A delegate set by
[`user.set_contract_accept_policy`](../ops/user.set_contract_accept_policy.md)
reads one from its input stream for each
[`user.accept_contract`](../ops/user.accept_contract.md) call that reaches the
contract accept policy: the node holds no active contract, and the contract
passes validation.

## Fields

* Caller (identity) – The caller of `user.accept_contract`.
* Contract
  ([`mod.auth.signed_contract`](../../auth/types/mod.auth.signed_contract.md)) –
  The node contract submitted for activation. Its issuer and subject signatures
  are verified, its subject is this node, and it carries a swarm membership
  permit.

## Example

```json
{
  "Type": "mod.user.contract_accept_request",
  "Object": {
    "Caller": "037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590",
    "Contract": {
      "Issuer": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
      "Subject": "037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590",
      "Permits": [
        {
          "Action": "mod.user.swarm_membership_action",
          "Constraints": null,
          "Delegation": 0
        }
      ],
      "ExpiresAt": "2027-05-27T10:00:00Z",
      "IssuerSig": "asn1:MEUCIQDg+5p9aT4q2QzVKbS9N5wXYrFh3vUaQ7E2lY0bX9pSAiB7H1k=",
      "SubjectSig": "asn1:MEQCIA1k0kZl0ZTd5KQv0pZL5kE2c8R5Mz0qY1g6kPq3rTfMAiB7H1k="
    }
  }
}
```
