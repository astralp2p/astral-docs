# mod.user.swarm_invite_request

The invitation a swarm invite policy decides. A delegate set by
[`user.set_swarm_invite_policy`](../ops/user.set_swarm_invite_policy.md) reads
one from its input stream for each
[`user.accept_membership`](../ops/user.accept_membership.md) call that reaches
the invite policy: the node holds no active contract, and the contract passes
validation, the expulsion check and issuer verification.

## Fields

* Inviter (identity) – The caller of `user.accept_membership`.
* Contract ([`mod.auth.contract`](../../auth/types/mod.auth.contract.md)) – The
  membership contract offered to this node. Its issuer signature is verified.

## Example

```json
{
  "Type": "mod.user.swarm_invite_request",
  "Object": {
    "Inviter": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
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
      "ExpiresAt": "2027-05-27T10:00:00Z"
    }
  }
}
```
