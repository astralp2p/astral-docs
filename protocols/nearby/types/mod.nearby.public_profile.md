# mod.nearby.public_profile

The node identity, user identity and alias that a node in mode `1` (Visible) discloses to every node on the local network.

## Fields

* NodeID (identity) – The node's identity (secp256k1 public key).
* UserID (identity, optional) – The identity of the node's user. Absent when the node has no owner.
* NodeAlias (string8) – The human-readable alias of the node. Empty when the node has no alias or its alias is longer than 255 bytes.

Each identity field is written as an optional value: a presence byte, `1` when the identity is present and `0` when it is absent, then the 33 key bytes when present ([Binary Encoding, Optional values](../../../topics/binary-encoding.md#optional-values)). JSON writes an absent `UserID` as `null`.

The profile states who the sender claims to be. The [`mod.nearby.status_proof`](mod.nearby.status_proof.md) of the same status proves that `NodeID` sent it. Only the user's contract proves that the node belongs to `UserID` ([`user.contract`](../../user/ops/user.contract.md)).

## Example

```json
{
  "Type": "mod.nearby.public_profile",
  "Object": {
    "NodeID": "035d6bfc7818844824354bd5ba1b7c08510139de14aa574e3f53a490814e3eab0e",
    "UserID": "02e8a0f652652cc090714d8fb3b26cddb33458106dd8a1edf6a9d870a9007fee55",
    "NodeAlias": "living-room"
  }
}
```
