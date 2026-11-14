# user.accept_membership

Accept a swarm membership contract sent by the issuer on the input stream. Answers an `error_message` reading `node already claimed` if the node already has an active contract. The contract is validated for subject identity match, an issuer distinct from the subject, minimum remaining validity, and a swarm-membership permit, then passed to the swarm invite policy; if approved, the node signs the contract, stores it, sets it as the active contract and indexes it, and only then answers its signature. Of concurrent invitations to one unclaimed node, one is set as the active contract; every other is answered `node already claimed` and receives no signature.

## Arguments

* (stream) – A `mod.auth.contract` object to evaluate, followed by a `mod.crypto.signature` carrying the issuer's signature.

## Returned objects

The operation returns one of:
* An `error_message` object if contract validation, policy check, issuer verification, signing, indexing, or storage fails.
* A `mod.crypto.signature` object containing the node's subject signature, sent after the node has stored, activated and indexed the contract.

## Examples

```shellsession
$ echo '{"Type":"mod.auth.contract","Object":{...}}' | astral-query user.accept_membership -in json -out json
{"Type":"mod.crypto.signature","Object":{"Data":"...","Scheme":"bip137"}}
```
