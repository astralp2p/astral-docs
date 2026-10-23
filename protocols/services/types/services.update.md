# services.update

One complete offering: what one provider offers one caller under one service
name.

An offering answers a particular caller. Two callers asking the same provider
for the same service can receive different updates. Each update replaces the
previous one for its [`services.offering_key`](services.offering_key.md)
whole; there are no partial updates.

`Available` false means the provider offers nothing to this caller. It is the
provider's answer, not a refusal: a refused discovery is an `error_message`
before any update. A [`services.discover`](../ops/services.discover.md) stream
sends `Available` false only for an offering it has shown as available, to
withdraw it. See
[Services § Reading the outcome](../../../topics/services.md#reading-the-outcome).

In a [`services.answer`](services.answer.md), `Name` must equal the `Service`
of the ask being answered; any other name fails the provider's binding.

`ProviderID` is the providing app identity, or the node identity for a service
the node itself offers. A provider leaves it empty in a
[`services.answer`](services.answer.md); the node sets it.

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
