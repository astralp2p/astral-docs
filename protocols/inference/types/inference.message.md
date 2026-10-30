# inference.message

One turn of a conversation.

`Role` is passed through as-is: "system", "user", "assistant" and "tool" are
the four every provider understands. A conversation is the ordered list of
messages in a request.

A tool call takes two kinds of turn. The assistant turn in which the model
called tools lists the calls in `ToolCalls`, as
[`inference.tool_call`](inference.tool_call.md) objects; its `Parts` hold any
text the model wrote beside them and may be empty. Then one "tool" turn per
call carries the result in `Parts`, and its `ToolCallID` names the call it
answers. A caller sends both back on every later request: the model sees what
it asked for next to what came back, and the IDs pair them when it made several
calls at once.

## Fields

* Role (string8) – "system", "user", "assistant" or "tool".
* Parts ([]inference.content_part) – The content of this turn, in order. May be empty on an assistant turn that only calls tools.
* ToolCalls ([]inference.tool_call) – The calls the model made in this turn, in order. Assistant turns only; empty otherwise.
* ToolCallID (string8) – The ID of the call this turn answers. Tool turns only; empty otherwise.

## Example

An assistant turn that called a tool:

```json
{
  "Type": "inference.message",
  "Object": {
    "Role": "assistant",
    "Parts": [],
    "ToolCalls": [
      {"ID": "call_1", "Name": "get_weather", "Arguments": "{\"city\":\"Lisbon\"}"}
    ],
    "ToolCallID": ""
  }
}
```

The result, as the tool turn that answers it:

```json
{
  "Type": "inference.message",
  "Object": {
    "Role": "tool",
    "Parts": [
      {"Kind": "text", "Text": "{\"temp_c\":24,\"sky\":\"clear\"}"}
    ],
    "ToolCalls": [],
    "ToolCallID": "call_1"
  }
}
```
