# user.swarm_digest

Answer the entry ID of every entry this node stores in SwarmState
([SwarmState synchronisation](../README.md#synchronisation)), then `eos`. A held
entry is not listed. The caller must be this node, the user, or an identity whose
membership holds in this node's SwarmState; the query of any other caller is
rejected. A node calls it on another node to learn what that node stores
before [`user.swarm_fetch`](user.swarm_fetch.md).

## Arguments

* out (string) – Optional output stream format (e.g. `json`).

## Returned objects

* An [`object_id`](../../../core-definitions/object-id.md) per stored entry, in
  no defined order.
* An `eos` after the last one.
