# user.new_node_contract

Build an unsigned `mod.auth.contract` from a user identity to a node identity
for a given duration. The contract carries three permits, in this order:
`mod.user.swarm_membership_action` with delegation 0, then
`mod.user.admin_swarm_action` and `mod.user.see_swarm_action` with delegation 1.
No permit carries constraints. Used by tooling that wants to assemble a
contract before asking the issuer and subject to sign it.

The operation answers `origin not allowed: network` to a query that arrived
over a [`Link`](../../../core-definitions/link.md). A remote party builds the
same contract client-side.

When `user` is omitted on a node with an active contract, the caller must hold
[`mod.user.see_swarm_action`](../types/mod.user.see_swarm_action.md), the action
`user.info` asks for the same identity. The operation answers `not permitted`
when the caller is not authorized. A caller that names `user` needs no action.

[`auth.sign_contract`](../../auth/ops/auth.sign_contract.md) signs this
contract, unmodified, for the node's own session while the node is unclaimed
and the contract's expiry is within the bounds that operation states. The
default duration is within them.

## Arguments

* user (string, optional) – Name or identity of the issuer (user). Defaults to
  this node's user (from the active contract).
* node (string, optional) – Name or identity of the subject (node). Defaults
  to the local node.
* duration (string, optional) – Go-style duration (e.g. `8760h`). Defaults to
  365 days (`8760h`).

## Returned objects

The operation returns one of:
* A `mod.auth.contract` ready to be signed.
* An `error_message` reading `origin not allowed: network` for a query from the
  network.
* An `error_message` reading `not permitted` if `user` is omitted on a node
  with an active contract and the caller does not hold
  `mod.user.see_swarm_action`.
* An `error_message` reading
  `user id missing: pass -user <identity>; the node has no active contract to default from`
  if `user` is omitted and the node has no active contract.
* An `error_message` reading `user id missing` if `user` resolves to the
  anonymous identity, as `anyone` does.
* An `error_message` if either identity could not be resolved, the duration
  failed to parse, or contract construction failed.

## Examples

```shellsession
$ astral-query user.new_node_contract -user alice -node laptop -duration 720h -out text
#[mod.auth.contract] ...
```
