# nat.hole

A pair of connected UDP endpoints resulting from a successful hole-punch, one held by the active (initiating) peer and one by the passive (responding) peer.

## Fields

* Nonce (nonce64) – Identifier of the hole, unique within the pool that holds it.
* ActiveIdentity ([`Identity`](../../../core-definitions/identity.md)) – The peer that initiated the punch.
* ActiveEndpoint (`nat.endpoint`) – The active peer's public UDP endpoint, as the passive peer observed it.
* ActiveBindPort (uint16) – The local UDP port the active peer binds for the hole.
* PassiveIdentity ([`Identity`](../../../core-definitions/identity.md)) – The peer that responded to the punch.
* PassiveEndpoint (`nat.endpoint`) – The passive peer's public UDP endpoint, as the active peer observed it.
* PassiveBindPort (uint16) – The local UDP port the passive peer binds for the hole.
* CreatedAt (time) – The moment the hole was created.

An endpoint is the address a peer sends to. A bind port is the port its owner binds. A NAT that translates ports makes a peer's endpoint port differ from its bind port. Each peer binds its own bind port to the hole's socket, and later to the kcp socket that consumes the hole, and sends to the other peer's endpoint.

## Example

```json
{
  "Type": "nat.hole",
  "Object": {
    "Nonce": "3fa1c0de9b7e0011",
    "ActiveIdentity": "037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590",
    "ActiveEndpoint": {
      "IP": "198.51.100.7",
      "Port": 41000
    },
    "ActiveBindPort": 41000,
    "PassiveIdentity": "02c4d3b2a1908f7e6d5c4b3a29180706f5e4d3c2b1a09f8e7d6c5b4a39281706f5",
    "PassiveEndpoint": {
      "IP": "203.0.113.10",
      "Port": 52000
    },
    "PassiveBindPort": 52000,
    "CreatedAt": "2026-07-08T12:00:00Z"
  }
}
```
