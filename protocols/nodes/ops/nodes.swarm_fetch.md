# nodes.swarm_fetch

Answer the stored SwarmState entries among the entry IDs the caller sends
([SwarmState](../README.md#swarmstate)). After accepting the query, the
operation reads [`object_id`](../../../core-definitions/object-id.md) objects
until an `eos`, then answers each stored entry among them, decoded as its
signed type, and an `eos`. An ID of no stored entry is skipped. The caller must
be this node, the user, or an identity whose membership holds in this node's
SwarmState; the query of any other caller is rejected. A pulling node asks for
at most 256 IDs per query.

## Arguments

* in (string) – Optional input stream format (e.g. `json`).
* out (string) – Optional output stream format (e.g. `json`).

## Returned objects

* Each stored entry the caller named: a
  [`mod.user.signed_contract_request`](../../user/types/mod.user.signed_contract_request.md),
  [`mod.user.signed_join_request`](../../user/types/mod.user.signed_join_request.md),
  [`mod.user.signed_expel_request`](../../user/types/mod.user.signed_expel_request.md),
  [`mod.user.signed_approval`](../../user/types/mod.user.signed_approval.md),
  [`mod.user.signed_decline`](../../user/types/mod.user.signed_decline.md),
  [`mod.auth.signed_contract`](../../auth/types/mod.auth.signed_contract.md) or
  [`mod.user.signed_expulsion`](../../user/types/mod.user.signed_expulsion.md).
* An `eos` after the last one.
