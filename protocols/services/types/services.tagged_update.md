# services.tagged_update

A [`services.update`](services.update.md) with its provider's effective
visibility, sent by a swarm member on a
[`services.discover`](../ops/services.discover.md) stream queried with `for`
and `tagged`. The requesting node reads `Open` to apply
[Visibility](../ops/services.discover.md#visibility) and forwards only the
`Update` to its caller.

`Open` is true when the provider's binding is open and no entry of the member's
[private list](mod.services.private_list.md) covers it. The member re-sends a
shown offering when `Open` changes.

## Fields

* Open (bool) – True if the provider is open on the member.
* Update ([`services.update`](services.update.md)) – The offering.

## Example

```json
{
  "Type": "services.tagged_update",
  "Object": {
    "Open": false,
    "Update": {
      "Available": true,
      "Name": "bitcoin-wallet",
      "ProviderID": "02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f",
      "Info": null
    }
  }
}
```
