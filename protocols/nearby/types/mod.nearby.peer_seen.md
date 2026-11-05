# mod.nearby.peer_seen

Emitted by nearby when a received status passes verification and its node is new to the cache, has a new source IP, or returns after its cache entry expired. It travels as the `Data` of a [`mod.events.event`](../../events/types/mod.events.event.md) to the node's own receivers and never leaves the node.

## Fields

* NodeID (identity) – The node that sent the status.
* UserID (identity, optional) – The node's user, as the recognizer or the `mod.nearby.public_profile` named it. Null when unknown.
* Via (string8) – The attachment the node was identified from: `hint` for a `mod.nearby.stealth_hint`, `profile` for a `mod.nearby.public_profile`.
* SourceIP ([`mod.ip.ip_address`](../../ip/types/mod.ip.ip_address.md)) – The IPv4 address the status came from.

The status proof shows that `NodeID` sent the status. It does not show that `NodeID` belongs to `UserID`; the user's contract shows that ([`user.contract`](../../user/ops/user.contract.md)).

A node in mode `0` (Silent) with `silent_listen` set to `false` emits no `mod.nearby.peer_seen`.

## Example

```json
{
  "Type": "mod.nearby.peer_seen",
  "Object": {
    "NodeID": "035d6bfc7818844824354bd5ba1b7c08510139de14aa574e3f53a490814e3eab0e",
    "UserID": "02e8a0f652652cc090714d8fb3b26cddb33458106dd8a1edf6a9d870a9007fee55",
    "Via": "hint",
    "SourceIP": "192.168.1.42"
  }
}
```
