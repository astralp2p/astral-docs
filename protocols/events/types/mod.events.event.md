# mod.events.event

The envelope of an event a node raises about its own state. See the
[`events`](../README.md) namespace for how events are delivered.

## Fields

* ID (nonce64) – Random identifier of this event.
* SourceID (identity) – Identity of the node that raised the event.
* Timestamp (time) – When the event was raised.
* Data (object) – The event object; any astral object type, encoded in its generic form (type + payload).

## Example

```json
{
  "Type": "mod.events.event",
  "Object": {
    "ID": "a1b2c3d4e5f60718",
    "SourceID": "02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f",
    "Timestamp": "2026-06-19T10:00:00Z",
    "Data": {
      "Type": "mod.nodes.link_created_event",
      "Object": {
        "RemoteIdentity": "037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590",
        "LinkID": "7c1a93b50f2e4d18",
        "LinkCount": 1
      }
    }
  }
}
```
