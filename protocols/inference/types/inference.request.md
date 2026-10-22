# inference.request

One completion, as the caller asks for it.

The request is the single input object of
[`inference.complete`](../ops/inference.complete.md). It names the model, says
how hard to think and how much output is acceptable, and carries the
conversation.

`System` is a convenience for the common single-prompt call; a leading message
with `Role` "system" is equivalent, and a request may use either.

`Temperature` is optional because "unset" and "0" mean different things: an
unset temperature is the model's own default, a zero is a demand for
determinism. A provider passes it through when the far side accepts it.

## Fields

* Model (string8) – The model to run, from `inference.models`.
* Effort (string8) – An effort level the model lists; empty takes the provider's default.
* MaxOutput (uint32) – A cap on output tokens for this request; 0 takes the model's `MaxOutput`.
* Temperature (float32) – Sampling temperature; absent means the model's default.
* Messages ([]inference.message) – The conversation, in order.
* System (string16) – A system prompt; empty carries none.
* Tools (string32) – A JSON array of tool definitions, passed through to the provider's far side; empty carries none.
* Stream (bool) – True asks for deltas; false asks for the whole answer in one chunk.

## Example

```json
{
  "Type": "inference.request",
  "Object": {
    "Model": "gpt-4o",
    "Effort": "medium",
    "MaxOutput": 2048,
    "System": "answer in one paragraph",
    "Messages": [
      {"Role": "user", "Parts": [{"Kind": "text", "Text": "why is the sky blue?"}]}
    ],
    "Stream": true
  }
}
```
