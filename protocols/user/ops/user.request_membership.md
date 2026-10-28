# user.request_membership

Request swarm membership from this node on behalf of the calling node. Answers an `error_message` reading `no active contract` if the node has no active contract. The swarm join-request policy is applied to the caller; if declined, an `error_message` is returned. On approval, a membership contract is issued for the caller, indexed, stored, and pushed to the local swarm asynchronously.

## Arguments

This operation takes no arguments.

## Returned objects

The operation returns one of:
* An `error_message` object if the join-request policy declines the caller, or if contract issuance, indexing, or storage fails.
* A `mod.auth.signed_contract` object containing the issued membership contract.

## Examples

```shellsession
$ astral-query user.request_membership -out json
{"Type":"mod.auth.signed_contract","Object":{...}}
```
