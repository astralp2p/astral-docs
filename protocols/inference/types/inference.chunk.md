# inference.chunk

One delta of an answer.

`Index` orders the chunks of one response, starting at 0 and increasing by one.
A consumer that renders text appends it; a consumer that records an answer keeps
the order the indexes give it, not the order frames arrived.

A chunk with a non-empty `FinishReason` is the last chunk of the answer. The
reason is the far side's — "stop", "length", or another value the provider
passes through — so a consumer can tell a finished answer from a truncated one.

`Reasoning` carries a model's thinking, kept apart from `Text` on purpose. A
consumer that renders answers ignores it; one that shows the thinking renders it
before the text it precedes. It is separate because a reasoning trace is not the
answer — joining them would make the answer unpresentable, and would hide from
the caller that the output budget was spent thinking. A provider that cannot
expose thinking leaves it empty, which is why a consumer must never infer an
answer's quality from its presence.

`Model` echoes the model that actually answered, set on the first chunk. It is
what lets a caller that offered a choice learn which one ran.

## Fields

* Index (uint32) – Position of this delta in the answer, from 0.
* Text (string16) – The delta itself; may be empty on the final chunk.
* Reasoning (string16) – The model's thinking, when the provider exposes it; empty otherwise. Never part of the answer.
* FinishReason (string8) – Empty while the answer continues; names why it ended on the last chunk.
* Model (string8) – The model that answered, set on the first chunk.

## Example

```json
{
  "Type": "inference.chunk",
  "Object": {
    "Index": 7,
    "Text": "scatters in every direction",
    "FinishReason": "",
    "Model": "gpt-4o"
  }
}
```
