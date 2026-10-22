# inference.models

Return the caller's inventory: every model this provider will serve *this
caller*, with its capabilities and effort levels.

The inventory is filtered to what the caller may use, so a caller never sees a
model it would be refused. A caller the provider does not serve at all has its
`Query` rejected rather than answered with an empty list — the two mean
different things, and an empty list would suggest the provider is running with
nothing to offer.

The same inventory is carried by the provider's `services` offering, so a
caller that reached the provider by discovery already has it. This operation
exists for a caller that knows the provider and wants a fresh one.

## Arguments

None.

## Returned objects

The operation returns one of:
* A rejected `Query`, before anything is sent, if the caller may not use this
  provider.
* One [`inference.models`](../types/inference.models.md) object, followed by an `eos` object.

## Examples

```shellsession
$ astral-query 02c00992…:inference.models -out json
{"Type":"inference.models","Object":{"Models":[{"ID":"gpt-4o","DisplayName":"GPT-4o","ContextWindow":128000,"MaxOutput":16384,"Modalities":["text","image"],"EffortLevels":[{"Name":"low","Description":"fastest, cheapest","TokenBudget":1024},{"Name":"high","Description":"most thorough","TokenBudget":8192}],"Streams":true,"Description":"general-purpose multimodal"}]}}
{"Type":"eos","Object":null}
```
