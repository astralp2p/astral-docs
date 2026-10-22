# inference.usage

What one completed request cost, in tokens.

The object follows the last chunk of an answer, and only when the provider's far
side reported figures. A provider that receives none sends no `inference.usage`
at all rather than a zero one: zeros would read as a free request, and the
absence reads as what it is — unmeasured.

## Fields

* PromptTokens (uint32) – Tokens the request's prompt consumed.
* CompletionTokens (uint32) – Tokens the answer produced.
* TotalTokens (uint32) – Their sum, as the provider reported it.

## Example

```json
{
  "Type": "inference.usage",
  "Object": {
    "PromptTokens": 412,
    "CompletionTokens": 96,
    "TotalTokens": 508
  }
}
```
