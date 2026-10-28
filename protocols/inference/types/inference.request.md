# inference.request

One completion, as the caller asks for it.

The request is the single input object of
[`inference.complete`](../ops/inference.complete.md). It names the model, says
how hard to think and how much output is acceptable, and carries the
conversation.

`System` is a convenience for the common single-prompt call; a leading message
with `Role` "system" is equivalent, and a request may use either. It is a
`string32`, as is every text a request carries, because a system prompt that
lists tools, rules and context easily outgrows 64 KiB.

`Temperature` is optional because "unset" and "0" mean different things: an
unset temperature is the model's own default, a zero is a demand for
determinism. A provider passes it through when the far side accepts it.

`Tools` lists the functions the model may call, as
[`inference.tool`](inference.tool.md) objects, and `ToolChoice` says whether it
must call one. Both are astral fields, not one vendor's JSON passed through: a
provider maps them onto whatever its server speaks, so a caller describes its
tools once for every provider. `ToolChoice` takes one of:

* empty or "auto" – the model decides whether to call;
* "none" – the model must not call any;
* "required" – the model must call at least one;
* a tool's `Name` – the model must call that tool.

A `ToolChoice` that names no tool in `Tools` is a bad request. Send tools only
to a model whose `Tools` is true; another model's server may refuse them or
ignore them.

## Fields

* Model (string8) – The model to run, from `inference.models`.
* Effort (string8) – An effort level the model lists; empty takes the model's `DefaultEffort`.
* MaxOutput (uint32) – A cap on output tokens for this request; 0 takes the model's `MaxOutput`.
* Temperature (optional float32) – Sampling temperature; absent means the model's default.
* Messages ([]inference.message) – The conversation, in order.
* System (string32) – A system prompt; empty carries none.
* Tools ([]inference.tool) – The functions the model may call; empty offers none.
* ToolChoice (string8) – Whether and which tool the model must call: empty or "auto", "none", "required", or a tool's `Name`.
* Stream (bool) – True asks for deltas; false asks for the whole answer in one chunk.

## Example

The second request of a tool loop: the model called `get_weather`, and the
caller sends the call and its result back with the conversation.

```json
{
  "Type": "inference.request",
  "Object": {
    "Model": "atlas-32b",
    "Effort": "low",
    "MaxOutput": 2048,
    "Temperature": null,
    "Messages": [
      {"Role": "user", "Parts": [{"Kind": "text", "Text": "is it warm in Lisbon?"}]},
      {"Role": "assistant", "Parts": [], "ToolCalls": [{"ID": "call_1", "Name": "get_weather", "Arguments": "{\"city\":\"Lisbon\"}"}]},
      {"Role": "tool", "Parts": [{"Kind": "text", "Text": "{\"temp_c\":24,\"sky\":\"clear\"}"}], "ToolCallID": "call_1"}
    ],
    "System": "answer in one sentence",
    "Tools": [
      {"Name": "get_weather", "Description": "the current weather in one city", "Parameters": "{\"type\":\"object\",\"properties\":{\"city\":{\"type\":\"string\"}},\"required\":[\"city\"]}"}
    ],
    "ToolChoice": "auto",
    "Stream": true
  }
}
```
