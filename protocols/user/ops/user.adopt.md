# user.adopt

Issue a swarm membership contract for the named node and return the signed result. The caller must hold `mod.user.admin_swarm_action`; the active contract's issuer holds it by default. Rejected with code `2` if the node has no active contract, with code `3` if `identity` does not resolve, and with code `4` if the caller is not authorized. After indexing, the signed contract is pushed to the local swarm asynchronously and a sync task is scheduled for the new member.

## Arguments

* identity (string8, required) – The node to adopt, given as a hex public key or a name resolved via the directory.

## Returned objects

The operation returns one of:
* An `error_message` object if identity resolution, contract issuance, indexing, or storage fails.
* A `mod.auth.signed_contract` object containing the issued membership contract.

## Examples

```shellsession
$ astral-query user.adopt -identity laptop -out json
{"Type":"mod.auth.signed_contract","Object":{...}}
```
