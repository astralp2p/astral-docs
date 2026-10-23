# services.answer

A provider's reply to one [`services.ask`](services.ask.md): the complete
offering of the asked service for the asked caller.

`RequestID` echoes the ask exactly.

`Update.Name` must equal the `Service` of the ask. This is a rule of the
protocol, not a convention: the node never fills or corrects the name. An
answer whose `Update.Name` differs from the asked service fails the binding.
The node closes the channel, every discovery stream shown one of the binding's
offerings receives a [`services.removed`](services.removed.md), and every
initial evaluation the binding still owed ends in a
[`services.incomplete`](services.incomplete.md).

`Update.ProviderID` is left empty; the node sets it to the binding's provider
identity. A non-empty `ProviderID` that differs from that identity, or a
missing `Update`, also fails the binding. An answer whose `RequestID` matches
no outstanding ask is ignored.

`Update.Available` false means the provider offers nothing to this caller. It is
an answer, not a failure, and the binding stays open. It differs from a refused
query, which means the caller may not ask at all — see
[Services § Reading the outcome](../../../topics/services.md#reading-the-outcome).

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
