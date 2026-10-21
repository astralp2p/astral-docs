# mod.ether.broadcast

The unsigned body of an ether broadcast: a single object announced to the broadcast network, tagged with who sent it and when. Wrap it in `mod.ether.signed_broadcast` before sending.

## Fields

* Timestamp (time) – When the broadcast was created.
* Source ([`Identity`](../../../core-definitions/identity.md)) – Identity of the node that originated the broadcast.
* Object (object) – The announced payload; any astral object type. On the wire it is length-prefixed (bytes16) and holds the object encoded in its generic form (type + payload).

## Example

```json
{
  "Type": "mod.ether.broadcast",
  "Object": {
    "Timestamp": "2026-06-19T10:00:00Z",
    "Source": "02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f",
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
