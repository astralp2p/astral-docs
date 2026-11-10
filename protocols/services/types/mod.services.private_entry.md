# mod.services.private_entry

One entry of a [`mod.services.private_list`](mod.services.private_list.md). It
covers the bindings of `ProviderID` that advertise `Service`. An empty
`ProviderID` covers every provider of `Service` on the node, native node
services included.

## Fields

* Service (string8) – The service name. Names follow the rules of [`services.advertise`](../ops/services.advertise.md).
* ProviderID (identity) – The provider covered; empty covers every provider.

## Example

```json
{
  "Type": "mod.services.private_entry",
  "Object": { "Service": "bitcoin-wallet", "ProviderID": null }
}
```
