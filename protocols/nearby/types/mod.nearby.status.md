# mod.nearby.status

A cached status of a nearby peer, combining the identity the receiver established for the peer with the attachments the peer sent.

## Fields

* Identity (identity, optional) – The node identity the receiver established for the peer, from a recognizer or from the peer's `mod.nearby.public_profile`. Null for a Stealth status that no recognizer matched.
* Attachments (bundle) – The attachments of the peer's last status, as received, the `mod.nearby.status_proof` included.

## Example

```json
{
  "Type": "mod.nearby.status",
  "Object": {
    "Identity": "035d6bfc7818844824354bd5ba1b7c08510139de14aa574e3f53a490814e3eab0e",
    "Attachments": [
      {
        "Type": "mod.nearby.flag",
        "Object": "adoptable"
      },
      {
        "Type": "mod.nearby.public_profile",
        "Object": {
          "NodeID": "035d6bfc7818844824354bd5ba1b7c08510139de14aa574e3f53a490814e3eab0e",
          "UserID": null,
          "NodeAlias": "living-room"
        }
      },
      {
        "Type": "mod.nearby.status_proof",
        "Object": {
          "Nonce": "3f9c2a7d11e4b605",
          "Timestamp": "2026-11-05T17:00:00Z",
          "Sig": "MEUCIQDrGjfIXhaxCzTaW42UztGuFdKoPVPe0LDlT+EUc9reXAIgAZ8y4LXgMO4WMYAwLOQ0ZtOk6To/hBflNDXtE8Zpfr0="
        }
      }
    ]
  }
}
```
