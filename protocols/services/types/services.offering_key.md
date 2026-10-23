# services.offering_key

The `(ProviderID, Name)` key of an offering. A provider can offer several
services; a service can have several providers.

## Fields

* ProviderID (identity) – The providing app identity, or the node identity for a service the node itself offers.
* Name (string8) – The service name.

## Example

```json
{
  "Type": "services.offering_key",
  "Object": {
    "ProviderID": "02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f",
    "Name": "player"
  }
}
```
