# services.removed

A notice on a [`services.discover`](../ops/services.discover.md) stream that
offerings the stream had shown are no longer valid because their provider was
lost, for example when its advertisement binding closed.

`Offerings` lists only keys previously sent on this stream as available. A
removal is distinct from a [`services.update`](services.update.md) with
`Available` false, which is the provider's own answer.

## Fields

* Offerings (array of [`services.offering_key`](services.offering_key.md)) – The offerings no longer valid.

## Example

```json
{
  "Type": "services.removed",
  "Object": {
    "Offerings": [
      {
        "ProviderID": "02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f",
        "Name": "player"
      }
    ]
  }
}
```
