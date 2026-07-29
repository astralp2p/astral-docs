# nat.list_holes

Stream the holes currently held in the local pool, optionally filtered to those involving a given peer. When `with` is supplied, only holes whose active or passive identity equals that peer are streamed; if `with` cannot be resolved to an identity the operation returns an `error_message` instead.

## Arguments

* with (string) – A peer identity, given as a hex public key or alias resolved via the directory. When set, only holes involving this peer are returned.

## Returned objects

The operation returns a stream of `nat.hole` objects, terminated by `eos`. If `with` is set and cannot be resolved to an identity, the operation returns an `error_message` object.

## Examples

```shellsession
$ astral-query nat.list_holes -out json
{"Type":"nat.hole","Object":{"Nonce":"3fa1c0de9b7e0011","ActiveIdentity":"037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590","ActiveEndpoint":{"IP":"198.51.100.7","Port":41000},"PassiveIdentity":"02c4d3b2a1908f7e6d5c4b3a29180706f5e4d3c2b1a09f8e7d6c5b4a39281706f5","PassiveEndpoint":{"IP":"203.0.113.10","Port":52000},"CreatedAt":"2026-07-08T12:00:00Z"}}
{"Type":"eos","Object":null}
```
