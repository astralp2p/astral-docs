# user.contract

Return the node's active contract to a caller that holds a direct link to the
node. A node that finds a peer of its own user through
[nearby](../../nearby/README.md) reads the peer's contract with this operation
and checks it before it introduces itself to the peer ([user](../README.md)).

The node refuses the query in these cases, in this order:

* The caller holds no direct link to this node: answered with an
  `error_message` reading `not permitted`.
* The node has no active contract: answered with `no active contract`.

The operation asks for no action. `mod.user.see_swarm_action` does not gate
it, and every caller with a direct link to the node passes the first check. A
session that calls with a user token calls as the user, which holds no link to
the node, and is answered `not permitted`.

## Disclosure

The contract names the node's user. Its permits show whether the node is a
management node ([user](../README.md)). Its expiry, by default 365 days after
the contract was made, shows when the user claimed or adopted the node. Every
node that links to this node reads the contract, also a node outside the
user's swarm. In mode `1` (Visible) every node on the local
network learns this node's identity from its
[`mod.nearby.public_profile`](../../nearby/types/mod.nearby.public_profile.md)
and can link to it. In mode `2` (Stealth) a node needs the node identity or
the user identity to recognise this node on the local network.

## Arguments

This operation takes no arguments.

## Returned objects

The query is answered with the `error_message` named in the cases above.
Otherwise the operation returns:
* A `mod.auth.signed_contract` holding the node's active contract.

## Examples

A session with the node's token calls as the node
([Session Identity, The node's token](../../../topics/session-identity.md#the-nodes-token)).
On a node linked to `03b1...`, it reads that node's contract:

```shellsession
$ export ASTRALD_APPHOST_TOKEN=<node token>
$ astral-query 03b1...:user.contract -out json
{"Type":"mod.auth.signed_contract","Object":{...}}
```
