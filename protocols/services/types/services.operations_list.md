# services.operations_list

The operations a provider exposes to one caller, carried in the `Info` bundle of
a [`services.update`](services.update.md).

Listing an operation grants nothing: the operation checks the caller's
permission when it runs. Whether the list is complete, and what an absent list
means, belongs to the service contract.

## Fields

* Operations (array of string8) – Operation names the caller may address to the provider.

## Example

```json
{
  "Type": "services.operations_list",
  "Object": { "Operations": ["player.play", "player.pause", "player.seek"] }
}
```
