# user.accept_contract

Activate a privileged membership the user key signed for this node, and this
node countersigned, as the node's active contract. Answers an `error_message`
reading `node already claimed` if the node already has an active contract. The
contract is validated — the issuer's signature, subject identity match, an
issuer distinct from the subject, remaining validity, exactly one tier permit
(`contract is not a membership` otherwise), the tier `privileged_member`
(`contract is not a privileged membership`), and this node's subject signature
(`contract lacks this node's signature`) — then stored and set as the active
contract. It is the activation step for node setup and the cold-card path: the
user key signs in the ceremony, and this node signs as subject only through
[`auth.sign_contract`](../../auth/ops/auth.sign_contract.md), whose claim rule
decides who may claim it.

## Arguments

* (stream) – A `mod.auth.signed_contract` object to activate.

## Returned objects

The operation returns one of:
* An `error_message` object if validation or storage fails.
* An `error_message` reading `the node has an active contract` if another
  claim completes after this query is accepted and before this claim.
* An `ack` object once the contract is stored and set as the active contract.

## Examples

```shellsession
$ echo '{"Type":"mod.auth.signed_contract","Object":{...}}' | astral-query user.accept_contract -in json -out json
{"Type":"ack","Object":{}}
```
