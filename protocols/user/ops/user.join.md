# user.join

Ask to join a user's swarm through `node`, a `trusted` or `privileged_member`
node of that swarm, its carrier. This node has no active contract. It signs a
[`mod.user.signed_join_request`](../types/mod.user.signed_join_request.md)
naming itself as `Joiner`, `node` as `Carrier` and `tier` as `Tier`, with the
default timeout of 1 hour, and keeps it in its tree until the join ends. It
sends the request to the carrier's [`user.carry_join`](user.carry_join.md) as
itself, with the `Network` [`Zone`](../../../core-definitions/zone.md), and
stays connected while the carrier signs the membership
([Joins](../README.md#joins)).

* The carrier answers the membership it signed as issuer. This node checks it
  against its request, signs it as subject and sends it back. The carrier adds
  the contract, with both signatures, to SwarmState and confirms it with the
  user identity. Only then does this node store the user identity, activate the
  membership and pull SwarmState from the carrier. The reply is the membership.
* The carrier issues `member` when it is `trusted` or `privileged_member`, and
  `trusted` when it is `privileged_member`. At tier `privileged_member` the user
  key signs the membership in a ceremony instead: on a Coldcard the user presses
  the device; with a software user key on the carrier, the user confirms with
  [`user.confirm_join`](user.confirm_join.md).
* A decline, the request's timeout, or a carrier that may not carry the request
  or issue the tier ends the join, and this node forgets the request.
* Any other failure, such as a dropped connection, keeps the request: the next
  `user.join` through the same carrier at the same tier resends the same
  request, with the same entry ID, and the carrier answers a membership with the
  same body. A join through another carrier is a new request.

The node refuses the query in these cases, in this order:

* The query's origin is `network`, `mcp` or any origin other than local:
  answered with an `error_message` reading `origin not allowed: <origin>`.
* The node has an active contract: answered with an `error_message` reading
  `node already claimed`.
* The caller is neither the node nor the node's
  [manager](../../sys/README.md#manager): answered with `not permitted`. A
  local caller that presents no identity is rewritten to the node's identity.
  The manager calls with its App token.
* `node` does not resolve: answered with an `error_message` reading
  `unknown identity`.
* `node` resolves to the anonymous identity: answered with `zero identity`.
* `node` names this node: answered with `cannot join self`.

The node adds the `Network` zone to its own query. A session without a token
reaches no other node, and still joins through this operation where the gate
admits it.

The default gate admits `user.join` on an `unclaimed` node from a session with
a token, and refuses it on a `fresh` node and from a session without a token
([Gate](../../apphost/README.md#gate)).

The join needs a route to the swarm node. Before the request the node looks
for one:

* A link to the swarm node, or an endpoint the node resolves for it, is a
  route, and the node sends the request at once.
* Otherwise the node broadcasts a
  [`mod.nearby.scan_message`](../../nearby/types/mod.nearby.scan_message.md)
  and waits up to 3 seconds, or to the query's deadline when that comes
  first. It checks for a route every 250 milliseconds and sends the request
  as soon as one appears, or when the wait ends without one. A node in
  Silent mode sends no scan and still waits.

While `user.join` runs, the node recognises the swarm node on a shared local
network through [`nearby`](../../nearby/README.md): its `user` module opens a
[`mod.nearby.stealth_hint`](../../nearby/types/mod.nearby.stealth_hint.md)
with the identity of the swarm node `node` names. A hint that opens names that
node and the user the hint carries. nearby then checks the status proof's
nonce and verifies its signature under the swarm node's key, as for every
recognised status, opens the sealed listen ports with the swarm node's
identity, and resolves the swarm node at the status's source IP on the `tcp`
and `kcp` ports the status carries, `1791` and `1792` when it carries none. A
swarm node in Visible mode names
itself in its profile and resolves the same way. A swarm node in Silent mode
answers no scan.

* The node opens hints with the swarm node's identity only, and only while
  `user.join` runs. A node with an active contract never opens a hint with a
  node identity.
* The node learns the swarm node's user identity from the hint before the
  swarm node admits it. Any node that knows a node identity can learn its
  user identity this way.

Elsewhere the swarm node provides the route. The default gate refuses
[`nodes.add_endpoint`](../../nodes/ops/nodes.add_endpoint.md) on an
`unclaimed` node, so this node cannot add the swarm node's endpoint before the
claim. The swarm node opens a link to this node with
[`nodes.new_link`](../../nodes/ops/nodes.new_link.md), and the join travels
over it. A swarm node on another network and one in Silent mode are reached
this way.
[User and Swarm, The route between the nodes](../../../topics/user-and-swarm.md#the-route-between-the-nodes)
shows the commands.

A join needs no answer in SwarmState: the carrier signs. A `privileged_member`
node may decline a join request at any tier, a `trusted` node one at tier
`member`, with [`user.answer_request`](user.answer_request.md); the request is
listed by [`user.swarm_requests`](user.swarm_requests.md).

## Arguments

* node (string8) – The carrier: a `trusted` or `privileged_member` node of the
  swarm to join, as a hex public key or a name, resolved as
  [`dir.resolve`](../../dir/ops/dir.resolve.md) does. Required.
* tier (string8) – The tier asked for: `member` (the default), `trusted` or
  `privileged_member`.
* in (string) – Optional input stream format (e.g. `json`).
* out (string) – Optional output stream format (e.g. `json`).

## Returned objects

The query is answered with the `error_message` named in the cases above.
Otherwise the operation returns one of:
* A `mod.auth.signed_contract` holding the membership. The node holds it as its
  active contract.
* An `error_message` reading `invalid tier` if `tier` names no tier.
* An `error_message` reading `join request declined` or `join request expired`
  when the request is declined or times out.
* An `error_message` reading `join request names another carrier` or `only a
  trusted or privileged member carries a join request` when the carrier may
  not carry it, and `tier above what this node may issue` when its tier may not
  issue the tier asked for.
* An `error_message` reading `a privileged membership needs the user key's
  signature` when the carrier reaches no user key for a `privileged_member`
  join.
* An `error_message` reading `route not found` if this node knows no route to
  the swarm node after the wait.
* An `error_message` reading `no active contract` if the carrier has no active
  contract.
* An `error_message` if the carrier cannot be reached, or if signing, storing
  or activating the membership fails.

## Examples

```shellsession
$ astral-query user.join -node 03b1... -tier member -out json
{"Type":"mod.auth.signed_contract","Object":{...}}
```
