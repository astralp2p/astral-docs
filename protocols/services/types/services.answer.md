# services.answer

A provider's reply to one [`services.ask`](services.ask.md): the complete
offering of the asked service for the asked caller.

`RequestID` echoes the ask exactly. `Update.Name` equals the asked service.
`Update.ProviderID` is left empty; the node sets it to the binding's provider
identity. A non-empty `ProviderID` that differs from that identity, a `Name`
that differs from the asked service, or a missing `Update` fails the binding.
An answer whose `RequestID` matches no outstanding ask is ignored.

`Update.Available` false means the provider offers nothing to this caller. It is
an answer, not a failure.

## Fields

* RequestID (nonce64) – The `RequestID` of the ask being answered.
* Update ([`services.update`](services.update.md)) – The complete offering for the asked caller.

## Example

```json
{
  "Type": "services.answer",
  "Object": {
    "RequestID": "9f2c41aa07d3e815",
    "Update": {
      "Available": true,
      "Name": "player",
      "ProviderID": null,
      "Info": [
        {
          "Type": "services.operations_list",
          "Object": { "Operations": ["player.play", "player.pause"] }
        }
      ]
    }
  }
}
```
