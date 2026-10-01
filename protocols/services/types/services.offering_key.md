# services.offering_key

The key of one offering: a provider identity and a service name. One provider
can offer several services, and several providers can offer one service, so an
offering is identified by both.

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
