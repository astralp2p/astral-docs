# user.carry_join

Carry the caller's join request into SwarmState and hand the caller its
membership once the request is answered. The caller is a node without an
active contract running [`user.join`](user.join.md); this node is its carrier.

After accepting the query, the operation reads one
[`mod.user.signed_join_request`](../types/mod.user.signed_join_request.md). It
must name the caller as `Joiner`, carry the joiner's signature, name this node
as `Carrier`, and name a valid tier. This node must hold a `trusted` or
`privileged_member` membership. The operation adds the request to SwarmState
(a resent request is stored already) and waits while the caller stays
connected:

* at tier `member` or `trusted`, until the request is not `pending`
  ([`user.swarm_requests`](user.swarm_requests.md)). On an approval it signs the
  joiner's membership at the request's tier, carrying out that approval
  (`ApprovalID`), valid no longer than its own membership, adds it to
  SwarmState and sends it. A membership it signed for that approval before is
  sent again instead;
* at tier `privileged_member`, until the user key has signed the joiner's
  privileged membership. With a Coldcard the key signs at once after the user
  presses the device; with a software user key held on this node, the user
  confirms with [`user.confirm_join`](user.confirm_join.md). A node that
  reaches no user key refuses.

A decline or the request's timeout ends the join. A dropped connection only
pauses it: the joiner resends the same request, and the operation runs the same
steps.

No action guards the operation: the caller holds nothing yet, and the carrier's
tier and the answer in SwarmState decide.

## Arguments

* in (string) – Optional input stream format (e.g. `json`).
* out (string) – Optional output stream format (e.g. `json`).

## Returned objects

* A `mod.auth.signed_contract` holding the joiner's membership, then the user
  identity (`identity`) the membership derives from.
* An `error_message` reading `no active contract` if this node is unclaimed.
* An `error_message` reading `not permitted` if the request does not name the
  caller as `Joiner`.
* An `error_message` reading `join request declined` or `join request expired`.
* An `error_message` reading `join request names another carrier`, `join
  request names an invalid tier`, `join request is not signed` or `only a
  trusted or privileged member carries a join request`.
* An `error_message` reading `a privileged membership needs the user key's
  signature` for a `privileged_member` request on a node that reaches no user
  key.
* An `error_message` if the request cannot be read, stored or carried out.
