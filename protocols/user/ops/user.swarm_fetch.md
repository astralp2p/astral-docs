# user.swarm_fetch

Answer the stored SwarmState entries among the entry IDs the caller sends
([SwarmState synchronisation](../README.md#synchronisation)). After accepting
the query, the operation reads [`object_id`](../../../core-definitions/object-id.md) objects
until an `eos`, then answers each stored entry among them, decoded as its
signed type, and an `eos`. An ID of no stored entry is skipped. The caller must
be this node, the user, or an identity whose membership holds in this node's
SwarmState; the query of any other caller is rejected. A query sends at most
256 IDs: when a 257th ID arrives, the operation answers an `error_message`
reading `too many IDs` and returns no entry. A pulling node asks for at most 256
IDs per query.

## Arguments

* in (string) – Optional input stream format (e.g. `json`).
* out (string) – Optional output stream format (e.g. `json`).

## Returned objects

* An `error_message` reading `too many IDs` if the caller sends more than 256
  IDs, or an `error_message` if the stream ends before the `eos`.
* Each stored entry the caller named: a
  [`mod.user.signed_contract_request`](../types/mod.user.signed_contract_request.md),
  [`mod.user.signed_join_request`](../types/mod.user.signed_join_request.md),
  [`mod.user.signed_expel_request`](../types/mod.user.signed_expel_request.md),
  [`mod.user.signed_approval`](../types/mod.user.signed_approval.md),
  [`mod.user.signed_decline`](../types/mod.user.signed_decline.md),
  [`mod.auth.signed_contract`](../../auth/types/mod.auth.signed_contract.md), a
  completed contract or a half-signed offer, or
  [`mod.user.signed_expulsion`](../types/mod.user.signed_expulsion.md).
* An `eos` after the last one.
