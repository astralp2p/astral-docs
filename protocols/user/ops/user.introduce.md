# user.introduce

Push this node's active contract to the node `identity` names, then
synchronise with that node. The named node checks the contract as it checks
every pushed node contract and indexes it, so this node becomes a member of the
named node's [`Local Swarm`](../../../core-definitions/local-swarm.md). The
reply is an `ack`.

`user.introduce` brings a node claimed with the user's words back into the
user's swarm. [`user.bootstrap`](user.bootstrap.md) leaves the node holding
its own contract alone: no other member holds that contract, and a node
synchronises with a linked node only when it holds that node's contract
([user](../README.md)). [User and Swarm, Replacing a node](../../../topics/user-and-swarm.md#replacing-a-node)
shows the whole path.

The node refuses the query in these cases, in this order:

* The query's origin is `network`: answered with an `error_message` reading
  `origin not allowed: network`.
* The node has no active contract: answered with `no active contract`.
* `identity` does not resolve: answered with `unknown identity`.
* `identity` resolves to the anonymous identity: answered with
  `zero identity`.
* `identity` names this node or the node's user: answered with
  `cannot introduce to self`.
* The caller does not hold `mod.user.admin_swarm_action` over the named node,
  or the user has expelled the caller: answered with `not permitted`.
  `identity` is resolved before the caller is authorized.
* The active contract has expired: answered with `contract expired`.
* The user has expelled the named node: answered with
  `identity expelled from swarm`.

The node then pushes its active contract to the named node with
[`objects.push`](../../objects/ops/objects.push.md), as itself, with the
`Network` [`Zone`](../../../core-definitions/zone.md), and waits at most 30
seconds for the answer. The named node refuses the contract when it has no
active contract, when its user is not this node's user, and when its user has
expelled this node. A refused or unanswered push is answered with an
`error_message` reading `push to <identity>: <reason>`, and no
synchronisation follows.

After an accepted push the node schedules a synchronisation with the named node
and answers `ack`. The answer does not wait for the synchronisation. The named
node, which now holds this node's contract and is linked to this node,
synchronises with this node as well. That synchronisation pushes the named
node's contract, the user's expulsions and the contracts of the other members
to this node. This node then links to the other members and synchronises
with each of them, and each member synchronises back once it holds this node's
contract.

* The named node's synchronisation is the only step that brings the other
  members' contracts to this node. No step of this node's own synchronisation
  reads contracts from the named node.
* A named node that does not synchronise when a pushed contract admits a linked
  node ([user](../README.md)) synchronises with this node at its next first
  link to this node. Closing the link
  ([`nodes.close_link`](../../nodes/ops/nodes.close_link.md)) and running
  `user.introduce` again opens a first link.
* This node reaches another member only over a link this node opens, to the
  endpoints the named node holds for that member.

## Gate

The default gate admits `user.introduce` on a `claimed` node from a session
with a token. The gate refuses it on a `fresh` or `unclaimed` node and from a
session without a token ([Gate](../../apphost/README.md#gate)). An
`apphost.yaml` that replaces the `claimed` list of `gate.states` lists
`user.introduce` for the op to run.

`gate.tokenless` never lists `user.introduce`. A local caller without a token
acts as the node, and a node that `user.bootstrap` claims holds
`mod.user.admin_swarm_action` by delegation, so the entry lets every local
program push the node's contract to any node.

## Disclosure

The named node reads this node's user from the pushed contract, also when the
named node is outside the swarm. A node outside the swarm refuses the contract
and indexes nothing. The pusher reads a bare refusal, which names no reason.

## Arguments

* identity (string8, required) – The node to introduce this node to: a hex
  public key or a name, resolved as
  [`dir.resolve`](../../dir/ops/dir.resolve.md) does. The named node is
  normally a running member of the user's swarm.
* in (string) – Optional input stream format (e.g. `json`).
* out (string) – Optional output stream format (e.g. `json`).

## Returned objects

The query is answered with the `error_message` named in the cases above.
Otherwise the operation returns one of:
* An `ack` once the named node accepted the contract. The synchronisation
  runs after the answer.
* An `error_message` reading `push to <identity>: <reason>` if the named node
  refuses the contract, cannot be reached, or does not answer within 30
  seconds.

## Examples

```shellsession
$ astral-query user.introduce -identity 03b1... -out json
{"Type":"ack","Object":null}
```
