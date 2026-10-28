# inference.complete

Run one completion and stream the answer back.

The caller sends exactly one [`inference.request`](../types/inference.request.md)
object on the channel. Everything the answer carries follows on the same channel:
an [`inference.chunk`](../types/inference.chunk.md) per delta, then an
[`inference.usage`](../types/inference.usage.md) when the far side reported one,
then `eos`. A refusal or a failure is an
[`inference.error`](../types/inference.error.md), then `eos`.

## Stream rules

* **Chunk order.** Chunks are indexed from 0 and increase by one. `Reasoning`,
  `Text` and `ToolCalls` may share a chunk.
* **Tool calls.** All deltas of one call carry the same `Index`, counting the
  answer's calls from 0. The call's `ID` and `Name` arrive on its first delta.
  Its `Arguments` pieces concatenate in order into one JSON object.
* **End of an answer.** The last chunk has a non-empty `FinishReason`: the far
  side's own reason, passed through. Then comes `inference.usage` when the far
  side reported usage, then `eos`.
* **Failures.**
  * Before the first chunk: one `inference.error`, then `eos`.
  * After some chunks: the chunks already sent stand, and the caller keeps the
    partial answer. One `inference.error` follows them, then `eos`. No chunk
    with a `FinishReason` precedes it, and no `inference.usage` follows it.
* **Every answer ends with `eos`.** A caller still reads EOF as the end of the
  response, as [op modes](../../../topics/op-modes.md) require of every client,
  and never blocks waiting for `eos`. What tells it whether the answer is whole
  is what came before: a chunk with a `FinishReason`, or an `inference.error`.
  A channel that ends with neither carries an answer that broke off — the
  provider or a link went away — and the caller treats it as a failure.
* **Broken order.** A chunk whose `Index` is not the next one, a chunk after the
  one with a `FinishReason`, and an `inference.usage` before that chunk or after
  another `inference.usage` break the answer too. The caller treats it as a
  failure and closes the channel.
* **Non-streaming** (`Stream: false`). One chunk, `Index` 0, carries the whole
  `Text`, the whole `Reasoning`, every tool call and the `FinishReason`. Each
  call is a single delta holding its ID, name and all of its arguments. Usage
  and `eos` follow as for a stream.

## Cancelling

Closing the channel cancels the request. The provider cancels the request to its
far side at once and releases the connection: while the server is still reading
the prompt, while the answer streams, and for a non-streaming request alike.
There is no separate cancel operation.

Promptness is the point. Reading a long prompt can occupy a server for minutes
before it produces a token, and a request nobody waits for any more must not
hold it that long.

## Admission

The caller must be allowed to use this provider and the model it names. The
check reads the caller's identity — the identity the node authenticated for the
query — and happens after the request is read and before any generation starts.
A refused caller receives an `inference.error` of Kind "refused", then `eos`,
and no output.

A request naming a model the provider does not offer, or one the caller may not
use, is refused the same way. A provider never substitutes a model.

Who a provider admits is described under
[design notes](../README.md#design-notes) in the protocol's README.

## Errors

A provider chooses the [`inference.error`](../types/inference.error.md) Kind by
what went wrong, so the caller can choose what to do next:

* "refused" – the caller is not admitted, or may not use the named model, or
  the provider does not offer it.
* "bad_request" – the channel carried no request; the request is malformed,
  e.g. a media part without a reference or a `ToolChoice` naming no tool in
  `Tools`; a media reference cannot be resolved or is one the provider will not
  take; or the far side rejected the request for another reason.
* "context_overflow" – the far side reports that the conversation and the output
  asked for exceed the model's context window.
* "rate_limited" – the far side or the provider limits requests; `RetryAfter`
  carries the wait when one is known.
* "unavailable" – the far side cannot be reached, or cannot take requests now.
* "far_side" – the far side failed otherwise, before or during the answer.

`Status` carries the far side's HTTP status and `Message` its message word for
word, whenever the error came from the far side.

## Arguments

None. The request travels as the channel's single input object.

## Returned objects

The operation returns one of:
* A stream of [`inference.chunk`](../types/inference.chunk.md) objects, the last
  with a non-empty `FinishReason`, then an optional
  [`inference.usage`](../types/inference.usage.md), then an `eos` object.
* An [`inference.error`](../types/inference.error.md) object, then an `eos`
  object, if the request is refused or fails before any output.
* A stream of `inference.chunk` objects, none with a `FinishReason`, then an
  `inference.error` object, then an `eos` object, if the far side fails after
  some output.

## Examples

A streamed answer:

```shellsession
$ astral-query 02c00992…:inference.complete -in json -out json <<'JSON'
{"Type":"inference.request","Object":{"Model":"atlas-32b","Effort":"off","Stream":true,
 "Messages":[{"Role":"user","Parts":[{"Kind":"text","Text":"why is the sky blue?"}]}]}}
JSON
{"Type":"inference.chunk","Object":{"Index":0,"Text":"Sunlight ","Reasoning":"","ToolCalls":[],"FinishReason":"","Model":"atlas-32b"}}
{"Type":"inference.chunk","Object":{"Index":1,"Text":"scatters ","Reasoning":"","ToolCalls":[],"FinishReason":"","Model":"atlas-32b"}}
{"Type":"inference.chunk","Object":{"Index":2,"Text":"…","Reasoning":"","ToolCalls":[],"FinishReason":"stop","Model":"atlas-32b"}}
{"Type":"inference.usage","Object":{"PromptTokens":12,"CompletionTokens":64,"TotalTokens":76,"CachedPromptTokens":0,"ReasoningTokens":0}}
{"Type":"eos","Object":null}
```

An answer that thinks, then calls a tool, its arguments split across chunks:

```shellsession
$ astral-query 02c00992…:inference.complete -in json -out json <<'JSON'
{"Type":"inference.request","Object":{"Model":"atlas-32b","Effort":"low","Stream":true,
 "Messages":[{"Role":"user","Parts":[{"Kind":"text","Text":"is it warm in Lisbon?"}]}],
 "Tools":[{"Name":"get_weather","Description":"the current weather in one city",
  "Parameters":"{\"type\":\"object\",\"properties\":{\"city\":{\"type\":\"string\"}},\"required\":[\"city\"]}"}]}}
JSON
{"Type":"inference.chunk","Object":{"Index":0,"Text":"","Reasoning":"I should check the weather.","ToolCalls":[],"FinishReason":"","Model":"atlas-32b"}}
{"Type":"inference.chunk","Object":{"Index":1,"Text":"","Reasoning":"","ToolCalls":[{"Index":0,"ID":"call_1","Name":"get_weather","Arguments":"{\"city\":\"Lis"}],"FinishReason":"","Model":"atlas-32b"}}
{"Type":"inference.chunk","Object":{"Index":2,"Text":"","Reasoning":"","ToolCalls":[{"Index":0,"ID":"","Name":"","Arguments":"bon\"}"}],"FinishReason":"tool_calls","Model":"atlas-32b"}}
{"Type":"inference.usage","Object":{"PromptTokens":88,"CompletionTokens":31,"TotalTokens":119,"CachedPromptTokens":64,"ReasoningTokens":9}}
{"Type":"eos","Object":null}
```

A conversation longer than the model's context window:

```shellsession
$ astral-query 02c00992…:inference.complete -in json -out json < long.json
{"Type":"inference.error","Object":{"Kind":"context_overflow","Status":400,"Message":"This model's maximum context length is 131072 tokens. However, you requested 140211 tokens.","RetryAfter":0}}
{"Type":"eos","Object":null}
```

The far side failing mid-answer:

```shellsession
$ astral-query 02c00992…:inference.complete -in json -out json < question.json
{"Type":"inference.chunk","Object":{"Index":0,"Text":"Sunlight ","Reasoning":"","ToolCalls":[],"FinishReason":"","Model":"atlas-32b"}}
{"Type":"inference.error","Object":{"Kind":"far_side","Status":0,"Message":"upstream stream ended without a finish reason","RetryAfter":0}}
{"Type":"eos","Object":null}
```
