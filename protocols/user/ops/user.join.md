# user.join

Ask a node of a swarm to admit this unclaimed node. The node sends
[`user.request_membership`](user.request_membership.md) to the node `node`
names, as itself, with the `Network` [`Zone`](../../../core-definitions/zone.md).
The swarm node's join policy decides the request. On admission the swarm node
issues a membership contract signed by its user and sends it to this node's
[`user.accept_membership`](user.accept_membership.md). This node's invite policy
decides the invitation; on acceptance this node signs as the subject, stores the
contract and sets it as the active contract. The reply is the signed contract
the swarm node returns.

`user.join` is the joining node's side of a membership. The swarm node's side is
[`user.adopt`](user.adopt.md), which sends the same contract to
`user.accept_membership` without a request.

The node refuses the query in these cases, in this order:

* The query's origin is `network`, `mcp` or any origin other than local:
  answered with an `error_message` reading `origin not allowed: <origin>`.
* The node has an active contract: answered with an `error_message` reading
  `node already claimed`.
* The caller is not the node: answered with `not permitted`. A local caller
  that presents no identity is rewritten to the node's identity.
* `node` does not resolve: answered with an `error_message` reading
  `unknown identity`.
* `node` resolves to the anonymous identity: answered with `zero identity`.
* `node` names this node: answered with `cannot join self`.

The node adds the `Network` zone to its own query. A session without a token
reaches no other node, and still joins through this operation.

The join policy of the swarm node and the invite policy of this node accept
everything by default ([user](../README.md)).

## Arguments

* node (string8) – The node of the swarm to join: a hex public key or a name,
  resolved as [`dir.resolve`](../../dir/ops/dir.resolve.md) does. Required.
* in (string) – Optional input stream format (e.g. `json`).
* out (string) – Optional output stream format (e.g. `json`).

## Returned objects

The query is answered with the `error_message` named in the cases above.
Otherwise the operation returns one of:
* A `mod.auth.signed_contract` holding the membership contract. The node holds
  it as its active contract.
* An `error_message` reading `request declined` if the swarm node's join policy
  declines this node.
* An `error_message` reading `invitation declined` if this node's invite policy
  declines the contract.
* An `error_message` reading `no active contract` if the swarm node has no
  active contract.
* An `error_message` if the swarm node cannot be reached, or if issuing,
  signing or storing the contract fails.

## Examples

```shellsession
$ astral-query user.join -node 03b1... -out json
{"Type":"mod.auth.signed_contract","Object":{...}}
```
