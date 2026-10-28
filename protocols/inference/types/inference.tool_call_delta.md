# inference.tool_call_delta

One piece of a tool call while the answer streams.

A model writes a call the way it writes text, a few tokens at a time, and a
caller that waits for the whole call before showing anything leaves its user
staring at nothing. So calls stream too, inside the
[`inference.chunk`](inference.chunk.md) that carries them, and the caller puts
each call together from its pieces:

* `Index` says which call of the answer a piece belongs to. Calls are numbered
  from 0 in the order they begin, and every piece of one call carries the same
  `Index`, so pieces of parallel calls never mix even when they interleave.
* `ID` and `Name` arrive on the call's first piece and are empty on the rest.
* `Arguments` pieces concatenate in the order they arrive. The text is a whole
  JSON object only once the answer has ended, so a caller parses it then, not
  before.

The assembled call is an [`inference.tool_call`](inference.tool_call.md). A
non-streaming answer carries each call as a single piece holding all of it.

## Fields

* Index (uint32) – Which call of this answer the piece belongs to, from 0.
* ID (string8) – The call's ID, on its first piece; empty otherwise.
* Name (string8) – The called tool's name, on its first piece; empty otherwise.
* Arguments (string32) – The next piece of the arguments text; may be empty.

## Example

The first piece of an answer's second call:

```json
{
  "Type": "inference.tool_call_delta",
  "Object": {
    "Index": 1,
    "ID": "call_2",
    "Name": "get_weather",
    "Arguments": "{\"city\":\"Por"
  }
}
```
