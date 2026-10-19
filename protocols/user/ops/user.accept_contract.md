# user.accept_contract

Activate a fully-signed contract as the node's active contract. Rejected with code `2` if the node already has an active contract. The contract is validated — both signatures, subject identity match, an issuer distinct from the subject, remaining validity, and a swarm-membership permit — then stored and set as the active contract. It is the activation step for node setup and the cold-card path, where the contract is already signed by both parties; the interactive counterpart is `user.accept_membership`.

## Arguments

* (stream) – A `mod.auth.signed_contract` object to activate.

## Returned objects

The operation returns one of:
* An `error_message` object if validation or storage fails.
* An `ack` object once the contract is stored and set as the active contract.

## Examples

```shellsession
$ echo '{"Type":"mod.auth.signed_contract","Object":{...}}' | astral-query user.accept_contract -in json -out json
{"Type":"ack","Object":{}}
```
