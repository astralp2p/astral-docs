# inference.models

Return the caller's inventory: every model this provider will serve *this
caller*, with its capabilities and effort levels.

The inventory is filtered to what the caller may use, so a caller never sees a
model it would be refused. A caller the provider does not serve at all receives
an [`inference.error`](../types/inference.error.md) of Kind "refused" rather
than an empty list — the two mean different things, and an empty list would
suggest the provider is running with nothing to offer. The error also tells the
caller why, where a rejected query would read the same as one that never
reached a provider.

The same inventory is carried by the provider's `services` offering, so a
caller that reached the provider by discovery already has it. This operation
exists for a caller that knows the provider and wants a fresh one.

## Arguments

None.

## Returned objects

The operation returns one of:
* One [`inference.models`](../types/inference.models.md) object, followed by an `eos` object.
* One [`inference.error`](../types/inference.error.md) object, followed by an
  `eos` object: "refused" if the caller may not use this provider, or another
  Kind if the provider cannot answer.

## Examples

```shellsession
$ astral-query 02c00992…:inference.models -out json
{"Type":"inference.models","Object":{"Models":[{"ID":"atlas-32b","DisplayName":"Atlas 32B","ContextWindow":131072,"MaxOutput":8192,"Modalities":["text","image"],"EffortLevels":[{"Name":"off","Description":"answer without thinking","TokenBudget":0},{"Name":"low","Description":"think briefly","TokenBudget":1024},{"Name":"high","Description":"think thoroughly","TokenBudget":8192}],"Streams":true,"Description":"general-purpose multimodal","DefaultEffort":"low","Tools":true}]}}
{"Type":"eos","Object":null}
```

A caller the provider does not admit:

```shellsession
$ astral-query 02c00992…:inference.models -out json
{"Type":"inference.error","Object":{"Kind":"refused","Status":0,"Message":"not permitted to use inference","RetryAfter":0}}
{"Type":"eos","Object":null}
```
