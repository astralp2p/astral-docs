# mod.ether.events.broadcast_received

Emitted locally when a broadcast arrives, has a valid signature, and is not the node's own. Carries the announced object together with the IP address the datagram came from.

## Fields

* SourceIP (bytes8) – The IP address the broadcast was received from (IPv4 stored as 4 bytes, IPv6 as 16 bytes).
* Object (object) – The announced payload; any astral object type, encoded in its generic form (type + payload).

## Example

```json
{
  "Type": "mod.ether.events.broadcast_received",
  "Object": {
    "SourceIP": "192.168.1.42",
    "Object": {
      "Type": "mod.nearby.status",
      "Object": {
        "Identity": "02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f",
        "Attachments": [
          {
            "Type": "mod.dir.alias",
            "Object": "alice"
          }
        ]
      }
    }
  }
}
```
