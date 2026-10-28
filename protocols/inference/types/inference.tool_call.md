# inference.tool_call

One call the model made, whole, as the conversation's history carries it.

While an answer streams, a call arrives in pieces — an
[`inference.tool_call_delta`](inference.tool_call_delta.md) at a time. A caller
assembles the pieces of one call into this object, runs the function, and on
the next request sends the call back in the assistant turn's `ToolCalls`,
followed by a `tool` turn whose `ToolCallID` names it. The model then sees what
it asked for next to what came back.

`ID` is what pairs a result with its call when the model made several at once.
It is unique within the answer that made the call; a provider whose server
gives a call no ID assigns one, because a call no result can name cannot be
answered.

`Arguments` is the JSON object the model wrote, as text. It is kept as the
model's own text rather than parsed into astral types because it is only as
well formed as the model made it: a caller validates it against the tool's
`Parameters` before running anything, and can show the model its own mistake
when it does not parse.

## Fields

* ID (string8) – Identifies the call within its answer; a `tool` turn's `ToolCallID` names it.
* Name (string8) – The [`inference.tool`](inference.tool.md) the model called.
* Arguments (string32) – A JSON object holding the arguments, as text.

## Example

```json
{
  "Type": "inference.tool_call",
  "Object": {
    "ID": "call_1",
    "Name": "get_weather",
    "Arguments": "{\"city\":\"Lisbon\"}"
  }
}
```
