# inference.chunk

One delta of an answer.

`Index` orders the chunks of one response, starting at 0 and increasing by one.
A consumer that renders text appends it; a consumer that records an answer keeps
the order the indexes give it, not the order frames arrived.

A chunk may carry any mix of `Reasoning`, `Text` and `ToolCalls`; a model that
thinks, says a word and starts a call within one server event delivers all three
in one chunk.

`ToolCalls` carries the model's calls in pieces, as
[`inference.tool_call_delta`](inference.tool_call_delta.md) objects. All pieces
of one call share its `Index`, its ID and name arrive on its first piece, and
its arguments are the concatenation of every piece's `Arguments`, in order. A
consumer puts each call together as the pieces arrive and runs it only once the
answer has ended.

A chunk with a non-empty `FinishReason` is the last chunk of the answer. The
reason is the far side's own — "stop", "length", "tool_calls",
"content_filter", or another value the provider passes through unchanged — so a
consumer can tell a finished answer from one cut off at the output limit, and an
answer that ends in calls to run from one that ends in prose.

`Reasoning` carries a model's thinking, kept apart from `Text` on purpose. A
consumer that renders answers ignores it; one that shows the thinking renders it
before the text it precedes. It is separate because a reasoning trace is not the
answer — joining them would make the answer unpresentable, and would hide from
the caller that the output budget was spent thinking. A provider that cannot
expose thinking leaves it empty, which is why a consumer must never infer an
answer's quality from its presence.

`Text` and `Reasoning` are `string32`, so a non-streaming answer, which carries
everything in one chunk, is never cut short by the field that holds it.

`Model` echoes the model that actually answered, set on the first chunk. It is
what lets a caller that offered a choice learn which one ran.

## Fields

* Index (uint32) – Position of this delta in the answer, from 0.
* Text (string32) – The answer's next piece; may be empty.
* Reasoning (string32) – The model's thinking, when the provider exposes it; empty otherwise. Never part of the answer.
* ToolCalls ([]inference.tool_call_delta) – Pieces of the tool calls the model is making; empty when this delta carries none.
* FinishReason (string8) – Empty while the answer continues; names why it ended on the last chunk.
* Model (string8) – The model that answered, set on the first chunk.

## Example

The last chunk of an answer that ends in a call:

```json
{
  "Type": "inference.chunk",
  "Object": {
    "Index": 7,
    "Text": "",
    "Reasoning": "",
    "ToolCalls": [
      {"Index": 0, "ID": "", "Name": "", "Arguments": "bon\"}"}
    ],
    "FinishReason": "tool_calls",
    "Model": "atlas-32b"
  }
}
```
