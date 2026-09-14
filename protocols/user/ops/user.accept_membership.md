# user.accept_membership

Accept a swarm membership contract sent by the issuer on the input stream. Rejected with code `2` if the node already has an active contract. The contract is validated for subject identity match and minimum remaining validity, then passed to the swarm invite policy; if approved, the node signs the contract and stores it as the active contract.

## Arguments

* (stream) – A `mod.auth.contract` object to evaluate, followed by a `mod.crypto.signature` carrying the issuer's signature.

## Returned objects

The operation returns one of:
* An `error_message` object if contract validation, policy check, issuer verification, signing, indexing, or storage fails.
* A `mod.crypto.signature` object containing the node's subject signature, sent after the invite policy approves and before the contract is indexed.

## Examples

```shellsession
$ echo '{"Type":"mod.auth.contract","Object":{...}}' | astral-query user.accept_membership -in json -out json
{"Type":"mod.crypto.signature","Object":{"Data":"...","Scheme":"bip137"}}
```
