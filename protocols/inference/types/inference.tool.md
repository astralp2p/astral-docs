# inference.tool

One function the model may call, as a request describes it.

A request lists its tools in `Tools`; a model that decides to use one answers
with [`inference.tool_call_delta`](inference.tool_call_delta.md) pieces instead
of, or beside, text. The caller runs the function and sends the result back as
a `tool` turn of the next request.

`Name` and `Description` are what the model reads to decide whether to call the
function at all, so the description is written for the model: what the
function does and when it helps.

`Parameters` is a JSON Schema object, carried as text. JSON Schema is the one
description of function arguments every tool-calling model server takes, and it
is a standard rather than any one vendor's format. Modelling it as astral types
instead would freeze a subset of an open-ended language — nested objects,
enumerations, references — and a provider would have to turn it back into JSON
for its server anyway. The provider passes the text through unchanged.

## Fields

* Name (string8) – The function's name, as the model calls it. Unique within a request.
* Description (string16) – What the function does and when to use it, for the model to read.
* Parameters (string32) – A JSON Schema object describing the arguments, as text; empty means the function takes none.

## Example

```json
{
  "Type": "inference.tool",
  "Object": {
    "Name": "get_weather",
    "Description": "the current weather in one city",
    "Parameters": "{\"type\":\"object\",\"properties\":{\"city\":{\"type\":\"string\"}},\"required\":[\"city\"]}"
  }
}
```
