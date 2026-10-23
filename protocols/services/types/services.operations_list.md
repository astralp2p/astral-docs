# services.operations_list

Operation names in a [`services.update`](services.update.md) `Info` bundle.
Each operation checks permission when invoked. The service contract defines
whether the list is complete and what an absent list means.

## Fields

* Operations (array of string8) – Operation names the caller may address to the provider.

## Example

```json
{
  "Type": "services.operations_list",
  "Object": { "Operations": ["player.play", "player.pause", "player.seek"] }
}
```
