# services.update

A complete, caller-specific offering. Each update replaces the previous value
for its [`(ProviderID, Name)` key](services.offering_key.md); partial updates
are not supported.

`Available: false` means the provider offers nothing to this caller.
[`services.discover`](../ops/services.discover.md) sends it only to withdraw a
previously shown offering. Initially unavailable offerings are omitted.
Permission refusal instead prevents evaluation; see
[consumer outcomes](../../../topics/services.md#reading-the-outcome).

In a [`services.answer`](services.answer.md), `Name` must equal the asked
`Service`; a mismatch fails the binding. The provider leaves `ProviderID`
empty or equal to its identity; the node fills it. Native node services carry
the node identity.

## Fields

* Available (bool) – True if the provider offers the service to this caller.
* Name (string8) – The service name. In a `services.answer`, the asked service exactly.
* ProviderID (identity) – The providing identity.
* Info (object) – A `bundle` of service-defined objects, such as a [`services.operations_list`](services.operations_list.md); may be empty.

## Example

```json
{
  "Type": "services.update",
  "Object": {
    "Available": true,
    "Name": "player",
    "ProviderID": "02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f",
    "Info": [
      {
        "Type": "services.operations_list",
        "Object": { "Operations": ["player.play", "player.pause"] }
      }
    ]
  }
}
```
