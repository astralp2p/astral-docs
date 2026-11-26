# user.introduce

Offer this node's active contract, its membership, to the SwarmState of the
node `identity` names, then synchronise with that node. The named node checks
the membership as it checks every SwarmState entry and stores it, so this node
becomes a member of the named node's
[`Local Swarm`](../../../core-definitions/local-swarm.md). The reply is an
`ack`.

`user.introduce` brings a node claimed with the user's words back into the
user's swarm. [`user.bootstrap`](user.bootstrap.md) leaves the node holding
its own contract alone: no other member lists that node, and a node
synchronises with a linked node only when its local swarm lists that node
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

The node then offers its active contract to the named node with
[`nodes.swarm_push`](../../nodes/ops/nodes.swarm_push.md), as itself, with the
`Network` [`Zone`](../../../core-definitions/zone.md), and waits at most 30
seconds for the answer. The named node drops the entry when its user did not
sign it and no member of its swarm may issue it, as a merge does
([SwarmState entries](../README.md#swarmstate-entries)); a membership of an
expelled node grants nothing there. A dropped or unanswered offer is answered
with an `error_message` reading `push to <identity>: <reason>`, and no
synchronisation follows.

After an accepted offer the node pulls the named node's SwarmState
([`nodes.swarm_digest`](../../nodes/ops/nodes.swarm_digest.md),
[`nodes.swarm_fetch`](../../nodes/ops/nodes.swarm_fetch.md)), schedules a
synchronisation with the named node and answers `ack`. A pull that fails does
not change the answer. The named node passes the stored membership on to its
peers, so the other members learn this node through SwarmState. The answer does not wait for the synchronisation. The named
node, which now lists this node and is linked to it, synchronises with this
node as well. That synchronisation pushes the user's expulsions and pulls this
node's SwarmState entries; it pushes no membership contracts. This node learns
the other members from the SwarmState it pulled, links to them and
synchronises with each of them, and each member synchronises back once its
local swarm lists this node.

* A named node that does not synchronise when an offered membership admits a
  linked node ([user](../README.md)) synchronises with this node at its next
  new link to this node. Running `user.introduce` again after closing the link
  ([`nodes.close_link`](../../nodes/ops/nodes.close_link.md)) opens a new link.
* This node reaches another member only over a link this node opens, to the
  endpoints the named node holds for that member.

## Gate

The default gate admits `user.introduce` on a `claimed` node from a session
with a token. The gate refuses it on a `fresh` or `unclaimed` node and from a
session without a token ([Gate](../../apphost/README.md#gate)). An
`apphost.yaml` that replaces the `claimed` list of `gate.states` lists
`user.introduce` for the op to run.

`gate.tokenless` never lists `user.introduce`. A local caller without a token
acts as the node, and a node that `user.bootstrap` claims holds a
`privileged_member` membership, so it answers `mod.user.admin_swarm_action`
through the swarm root, and the entry lets every local program push the node's
contract to any node.

## Disclosure

The named node reads this node's user from the offered membership, also when
the named node is outside the swarm. A node outside the swarm drops the entry
and stores nothing. The node reads `swarm entry dropped` with the entry's ID,
which names no reason.

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
* An `ack` once the named node accepted the membership. The synchronisation
  runs after the answer.
* An `error_message` reading `push to <identity>: <reason>` if the named node
  drops the membership, cannot be reached, or does not answer within 30
  seconds.

## Examples

```shellsession
$ astral-query user.introduce -identity 03b1... -out json
{"Type":"ack","Object":null}
```
