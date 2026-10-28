# inference.usage

What one completed request cost, in tokens.

The object follows the last chunk of an answer, and only when the provider's far
side reported figures. A provider that receives none sends no `inference.usage`
at all rather than a zero one: zeros would read as a free request, and the
absence reads as what it is — unmeasured. Within the object, a field the far
side did not report is 0.

`CachedPromptTokens` and `ReasoningTokens` are parts of the two totals, not
additions to them. Hosted servers commonly bill cached prompt tokens at a
lower price, and tokens spent thinking count as output the caller never sees,
so a consumer that prices a request or explains its cost needs both.

## Fields

* PromptTokens (uint32) – Tokens the request's prompt consumed.
* CompletionTokens (uint32) – Tokens the answer produced, thinking included.
* TotalTokens (uint32) – Their sum, as the provider reported it.
* CachedPromptTokens (uint32) – Of `PromptTokens`, those the server read from its prompt cache.
* ReasoningTokens (uint32) – Of `CompletionTokens`, those spent thinking.

## Example

```json
{
  "Type": "inference.usage",
  "Object": {
    "PromptTokens": 412,
    "CompletionTokens": 96,
    "TotalTokens": 508,
    "CachedPromptTokens": 384,
    "ReasoningTokens": 40
  }
}
```
