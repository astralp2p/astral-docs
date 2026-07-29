# nat.punch

Drive the initiator side of a NAT hole-punch against a target identity and register the resulting hole. The node resolves its own public IPv4 address and the target identity, then runs the offer/answer/ready/go/result exchange with the target's `nat.node_punch` operation. The operation fails if the node has no suitable public IPv4 address, if the target identity cannot be resolved, or if any step of the punch does not complete.

## Arguments

* target (string, required) – The peer to punch to, given as a hex public key or alias resolved via the directory.

## Returned objects

The operation returns one of:
* An `error_message` object if the local IP or target identity cannot be resolved, or the punch fails.
* A single `nat.hole` object describing the connected endpoint pair on success.

## Examples

```shellsession
$ astral-query nat.punch -target 02c4d3b2a1908f7e6d5c4b3a29180706f5e4d3c2b1a09f8e7d6c5b4a39281706f5 -out json
{"Type":"nat.hole","Object":{"Nonce":"3fa1c0de9b7e0011","ActiveIdentity":"037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590","ActiveEndpoint":{"IP":"198.51.100.7","Port":41000},"PassiveIdentity":"02c4d3b2a1908f7e6d5c4b3a29180706f5e4d3c2b1a09f8e7d6c5b4a39281706f5","PassiveEndpoint":{"IP":"203.0.113.10","Port":52000},"CreatedAt":"2026-07-08T12:00:00Z"}}
```
