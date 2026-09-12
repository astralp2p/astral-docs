# nat.node_punch

Run the passive (participant) side of a NAT hole-punch with the calling peer. The operation punches a hole with the caller identity itself, so it takes no target argument. Over the channel it receives the caller's `nat.punch_signal` of type `offer`, replies `answer`, receives `ready`, replies `go`, performs the simultaneous UDP punch, then receives and echoes the final `result` signal. On success the resulting hole is registered locally and no further object is returned. The operation fails if the node has no suitable public IPv4 address, or if any signal is out of order, carries a mismatched session, or the punch does not complete.

The caller must hold
[`mod.auth.admin_network_action`](../../auth/types/mod.auth.admin_network_action.md).
The query is rejected before any puncher socket is opened when the caller is not
authorized, and a refused caller receives no bytes.

## Arguments

This operation takes no arguments beyond the implicit input and output format hints.

## Returned objects

The operation exchanges `nat.punch_signal` control messages with the caller over the channel. It returns no object on success; it returns an `error_message` object if a signal is unexpected or the punch fails.

## Examples

```shellsession
$ astral-query nat.node_punch -out json
```
