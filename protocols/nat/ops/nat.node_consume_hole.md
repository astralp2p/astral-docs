# nat.node_consume_hole

Hand a hole out of the local pool through a two-phase lock-then-take handshake. The node first removes the hole named by `pair` from its pool; if no hole with that nonce exists the operation fails. The role depends on `target`: when `target` is set the node acts as the initiator, opens `nat.node_consume_hole` on the target, locks the hole, and returns an `ack`; when `target` is omitted the node acts as the responder and drives the exchange over the channel, receiving a `lock` `nat.consume_hole_signal`, replying `locked`, receiving `take`, replying `taken`, and finally returning the `nat.hole`. The operation fails if the hole is already locked by another consumer or the handshake does not complete.

## Arguments

* pair (nonce64, required) – The nonce of the hole to consume.
* target (string) – When set, the peer to coordinate with, given as a hex public key or alias resolved via the directory; the node then acts as initiator. When omitted, the node acts as responder.

## Returned objects

The operation returns one of:
* An `error_message` object if the hole does not exist, is busy, the target cannot be resolved, or the handshake fails.
* An `ack` object when `target` was set and the hole was locked successfully.
* A single `nat.hole` object when `target` was omitted and the responder handshake completed. In the responder role the node also exchanges `nat.consume_hole_signal` control messages with the caller over the channel.

## Examples

```shellsession
$ astral-query nat.node_consume_hole -pair 3fa1c0de9b7e0011 -target 02c4d3b2a1908f7e6d5c4b3a29180706f5e4d3c2b1a09f8e7d6c5b4a39281706f5 -out json
{"Type":"ack","Object":null}
```
