# inference.effort_level

One settable effort of one model.

Effort is what a caller chooses between when it does not want to reason about
tokens: a name with an agreed meaning, and a provider that decides how to spend
it. A provider maps a level onto whatever its far side honours — a reasoning
parameter, a cap on output, or nothing at all when the model has no such knob.
The level is the contract; the mapping is not.

One name has a fixed meaning: `off` is the level at which the model does not
think at all. A model that can be told so lists it, usually first, so a caller
that wants a plain answer fast asks for it by name instead of guessing which
level is the lowest.

## Fields

* Name (string8) – The level, e.g. "off", "low", "medium", "high", or a provider-defined name.
* Description (string8) – What the level means for this model, in words.
* TokenBudget (uint32) – An expected output budget in tokens, or 0 when the provider states no figure.

## Example

```json
{
  "Type": "inference.effort_level",
  "Object": {
    "Name": "high",
    "Description": "most thorough; slowest and most expensive",
    "TokenBudget": 8192
  }
}
```
