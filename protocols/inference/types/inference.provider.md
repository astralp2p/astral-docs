# inference.provider

Who is offering: the name and description the provider's operator chose.

A provider is an app, and an app's identity is a public key — right for
addressing a query, useless for telling a person which provider a model runs
on. This object travels in the provider's `services` offering, beside the
[`inference.models`](inference.models.md) inventory, so a consumer that lists
providers shows a name from the same round trip that found them.

The name is the operator's word, not a claim the network checks: two providers
may carry the same one. A consumer that needs to tell them apart keeps the
identity alongside, and one that receives an empty `Name` falls back to
something it can resolve itself, such as the alias of the provider's node.

## Fields

* Name (string8) – A short name the operator chose, e.g. "ai0"; empty when none was set.
* Description (string16) – Free text about the provider, or empty.

## Example

```json
{
  "Type": "inference.provider",
  "Object": {
    "Name": "ai0",
    "Description": "the GPU box in the office; local models only"
  }
}
```
