# services.answer

A provider's complete answer to a [`services.ask`](services.ask.md).
`RequestID` must echo the ask. Answers without an outstanding request, including
late answers, are ignored.

For a matching request:

* `Update` is required; `Update.Name` must equal the asked `Service` exactly.
* `Update.ProviderID` is empty or equals the binding's provider. The node fills
  it with that identity.
* `Update.Available: false` means nothing is offered to the caller. The binding
  stays open; this differs from [discovery refusal](../../../topics/services.md#reading-the-outcome).

A missing update, mismatched name, or different provider fails the binding.
Closure sends [`services.removed`](services.removed.md) for shown offerings
and marks unresolved initial evaluations in
[`services.incomplete`](services.incomplete.md).

## Fields

* RequestID (nonce64) – The `RequestID` of the ask being answered.
* Update ([`services.update`](services.update.md)) – The complete offering for the asked caller. Its `Name` equals the ask's `Service`.

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
