# inference.complete

Run one completion and stream the answer back.

The caller sends exactly one [`inference.request`](../types/inference.request.md)
object on the channel. Everything the answer carries follows on the same channel:
an [`inference.chunk`](../types/inference.chunk.md) per delta, then an optional
[`inference.usage`](../types/inference.usage.md), then `eos`.

Chunks are indexed from zero and increase by one. A chunk carrying a non-empty
`FinishReason` is the last of the answer; the `usage` object, when the provider
reports one, follows it. A client reads until `eos` or EOF, and never blocks
waiting for `eos`.

Closing the channel cancels the request: the provider stops generating and
releases the upstream connection.

## Admission

The caller must be allowed to use this provider and the model it names. The
check reads the caller's identity — the identity the node authenticated for the
query — and happens after the request is read and before any generation starts.
A refused caller receives an `error_message` and no output.

A request naming a model the provider does not offer, or one the caller may not
use, is refused the same way. A provider never substitutes a model.

## Arguments

None. The request travels as the channel's single input object.

## Returned objects

The operation returns one of:
* An `error_message` object if the caller is not allowed, the model is unknown,
  a media reference cannot be resolved, or the far side fails before any output.
* A stream of [`inference.chunk`](../types/inference.chunk.md) objects, then an
  optional [`inference.usage`](../types/inference.usage.md), then an `eos` object.

An upstream failure after some chunks were sent is reported as a trailing
`error_message`; the chunks already delivered stand, and the caller keeps the
partial answer.

## Examples

```shellsession
$ astral-query 02c00992…:inference.complete -in json -out json <<'JSON'
{"Type":"inference.request","Object":{"Model":"gpt-4o","Effort":"low","Stream":true,
 "Messages":[{"Role":"user","Parts":[{"Kind":"text","Text":"why is the sky blue?"}]}]}}
JSON
{"Type":"inference.chunk","Object":{"Index":0,"Text":"Sunlight ","FinishReason":"","Model":"gpt-4o"}}
{"Type":"inference.chunk","Object":{"Index":1,"Text":"scatters ","FinishReason":"","Model":"gpt-4o"}}
{"Type":"inference.chunk","Object":{"Index":2,"Text":"…","FinishReason":"stop","Model":"gpt-4o"}}
{"Type":"inference.usage","Object":{"PromptTokens":12,"CompletionTokens":64,"TotalTokens":76}}
{"Type":"eos","Object":null}
```
