# user.accept_contract

Activate a fully-signed contract as the node's active contract. Answers an `error_message` reading `node already claimed` if the node already has an active contract. The contract is validated — both signatures, subject identity match, an issuer distinct from the subject, remaining validity, and a swarm-membership permit — then decided by the contract accept policy, then stored and set as the active contract. It is the activation step for node setup and the cold-card path, where the contract is already signed by both parties; the interactive counterpart is `user.accept_membership`.

The contract accept policy accepts every contract that passes validation by
default, so a node out of the box is claimable.
[`user.set_contract_accept_policy`](user.set_contract_accept_policy.md)
delegates the decision to an operation of another identity, which receives a
[`mod.user.contract_accept_request`](../types/mod.user.contract_accept_request.md).
The wait for the delegate also ends when the caller disconnects.

## Arguments

* (stream) – A `mod.auth.signed_contract` object to activate.

## Returned objects

The operation returns one of:
* An `error_message` object if validation or storage fails.
* An `error_message` reading `contract declined` if the contract accept
  policy declines the contract, or its delegate cannot be reached or answers
  nothing within its timeout.
* An `error_message` reading `the node has an active contract` if another
  claim completes after this query is accepted and before this claim.
* An `ack` object once the contract is stored and set as the active contract.

## Examples

```shellsession
$ echo '{"Type":"mod.auth.signed_contract","Object":{...}}' | astral-query user.accept_contract -in json -out json
{"Type":"ack","Object":{}}
```
