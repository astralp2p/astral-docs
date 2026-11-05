# mod.ether.events.broadcast_received

Delivered by the node to its own object receivers, as the node itself, when an ether datagram passes the receive checks and is not the node's own: its source IP is not one of the node's addresses. Carries the object the datagram's envelope held together with the IP address the datagram came from. It names no remote identity and carries no signature.

## Fields

* SourceIP ([`mod.ip.ip_address`](../../ip/types/mod.ip.ip_address.md)) – The IPv4 address the datagram came from, stored as 4 bytes.
* Object (object) – The object the datagram's [`mod.ether.envelope`](mod.ether.envelope.md) held; any astral object type, encoded in its generic form (type + payload).

## Example

A Visible status of a node without an owner:

```json
{
  "Type": "mod.ether.events.broadcast_received",
  "Object": {
    "SourceIP": "192.168.1.42",
    "Object": {
      "Type": "mod.nearby.status_message",
      "Object": {
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
  }
}
```
