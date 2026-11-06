# user.adopt

Issue a swarm membership contract for the named node and return the signed result. The caller must hold `mod.user.admin_swarm_action`; the active contract's issuer holds it by default. Answers an `error_message` reading `no active contract` if the node has no active contract. Answers an `error_message` reading `unknown identity` if `identity` does not resolve, and `zero identity` if it resolves to the anonymous identity. Answers `not permitted` if the caller is not authorized. After indexing, the signed contract is pushed to the local swarm asynchronously and a sync task is scheduled for the new member.

The node sends the contract to the adopted node's
[`user.accept_membership`](user.accept_membership.md) and needs a route to it:
[`nodes.add_endpoint`](../../nodes/ops/nodes.add_endpoint.md) on this node
names the adopted node's endpoint, unless the two nodes share a local network
and find each other through [`nearby`](../../nearby/README.md). The adopted
node's invite policy decides the contract and declines it by default
([user](../README.md)).
[User and Swarm, The route between the nodes](../../../topics/user-and-swarm.md#the-route-between-the-nodes)
shows the commands.

## Arguments

* identity (string8, required) – The node to adopt, given as a hex public key or a name resolved via the directory.

## Returned objects

The operation returns one of:
* An `error_message` object if identity resolution, contract issuance, indexing, or storage fails.
* A `mod.auth.signed_contract` object containing the issued membership contract.
* An `error_message` reading `invitation declined` if the adopted node's invite
  policy declines the contract.

## Examples

```shellsession
$ astral-query user.adopt -identity laptop -out json
{"Type":"mod.auth.signed_contract","Object":{...}}
```
