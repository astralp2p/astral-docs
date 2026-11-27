# user.swarm_push

Offer one SwarmState entry to this node
([SwarmState synchronisation](../README.md#synchronisation)). After accepting
the query, the operation reads one entry and adds it as a merge: the merge check
decides it ([SwarmState entries](../README.md#swarmstate-entries)), and an
accepted entry is stored and passed on to this node's linked swarm members. Any caller with an identity may offer an
entry; a query without one is rejected.

## Arguments

* in (string) – Optional input stream format (e.g. `json`).
* out (string) – Optional output stream format (e.g. `json`).

## Returned objects

* An `ack` when the entry is stored, or was stored already.
* An `error_message` reading `swarm entry held until what it needs arrives`
  when the entry waits: it is held and checked again after the next merge.
* An `error_message` beginning `swarm entry dropped` when the check drops it.
* An `error_message` when the object is not an entry, or the store fails.
