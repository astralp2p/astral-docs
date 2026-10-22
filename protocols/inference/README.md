# inference

The `inference` protocol lets a client ask an astral node to generate text — or
anything a model can produce from text, images, audio and video — and to learn
first what models are on offer and what they cost to run.

The provider on the far side speaks an OpenAI-compatible API. The near side is
astral-native: an app advertises a service, a caller discovers it, and one
channel carries a request and its streamed answer.

## Design notes

* **Discovery is the inventory.** A provider advertises itself as the
  [`services`](../services/README.md) service named `inference`. Its offering's
  `Info` bundle carries an [`inference.models`](types/inference.models.md)
  object, so a caller learns the model list, each model's context window, output
  ceiling, supported modalities and effort levels in the same round trip that
  finds the provider. There is no second call to make before the first one.
  [`inference.models`](ops/inference.models.md) exists for a caller that already
  knows a provider and wants the inventory again, or a fresher one.

* **The offering is per caller.** A provider evaluates each caller on its own,
  exactly as [`services`](../../topics/services.md) defines an offering. A caller
  the provider will not serve is shown no offering at all — not an empty one —
  and a caller it will serve sees only the models it may use. An inventory is
  therefore never global, and a client must not cache one across callers.

* **Everything is gated on the caller's identity.** Authorization reads the
  caller of the incoming query, never anything the caller says about itself. By
  default the local User identity and the local node identity are allowed; every
  other caller needs an explicit allowance. A caller asks its own node, so the
  identity the provider sees is the one the node authenticated, whether the
  query came from a local app, the CLI, or across a [`Link`](../../core-definitions/link.md).

* **Effort is a first-class field, not a passthrough.** A model lists the effort
  levels it honours — `low`, `medium`, `high`, or provider-defined names — each
  with a description and an optional token budget hint. The consumer chooses
  between named levels; how the provider realises one on its far side (a
  reasoning-effort parameter, a token cap, or nothing at all) is its business. A
  passthrough of one vendor's parameter would leak that vendor into the protocol
  and mean nothing to a caller facing a different far side.

* **Media is referenced, not re-sent.** A content part carries media in one of
  three ways. *Inline* bytes suit a small picture the client already holds.
  *Object* names an [`object_id.sha256`](../../core-definitions/object-id.md) the
  network already addresses, and the provider reads it once through
  [`objects.read`](../objects/ops/objects.read.md) — so a caller that has the
  media on the network never uploads it again, and a provider can serve the same
  asset to many callers from one copy. *URL* names an address the provider is
  allowed to fetch itself. This is what makes multimodal calls reasonable on a
  network where a byte that is addressable need not be transported twice.

* **Streaming is the default.** [`inference.complete`](ops/inference.complete.md)
  is a channel operation: the caller sends one request and reads
  [`inference.chunk`](types/inference.chunk.md) deltas in `Index` order, then an
  optional [`inference.usage`](types/inference.usage.md), then `eos`. Chunks are
  indexed from zero and increase by one; a chunk with a non-empty `FinishReason`
  is the last of the answer. Per
  [op modes](../../topics/op-modes.md), a client never blocks waiting for `eos`:
  EOF is a legitimate end of any response.

* **Closing the channel cancels the work.** A caller that stops reading, or
  closes its channel, cancels the request upstream and the provider releases the
  far-side connection. There is no separate cancel operation.

## Discovery

```shellsession
$ astral-query services.discover -services inference -out json
{"Type":"services.update","Object":{"Available":true,"Name":"inference","ProviderID":"02c00992…","Info":[{"Type":"inference.models","Object":{"Models":[{"ID":"gpt-4o","ContextWindow":128000,"MaxOutput":16384,"Modalities":["text","image"],"EffortLevels":[{"Name":"low","Description":"fastest","TokenBudget":1024}],"Streams":true}]}},{"Type":"services.operations_list","Object":{"Operations":["inference.models","inference.complete"]}}]}}
{"Type":"eos","Object":null}
```

A caller that is not allowed sees no offering from that provider. A provider
that serves several callers differently shows each of them a different
inventory.

## Operations

* [inference.models](ops/inference.models.md) – the caller's inventory, again
* [inference.complete](ops/inference.complete.md) – run one completion, streaming

## Types

* [inference.model](types/inference.model.md) – one model and its capabilities
* [inference.models](types/inference.models.md) – an inventory
* [inference.effort_level](types/inference.effort_level.md) – one settable effort
* [inference.request](types/inference.request.md) – one completion request
* [inference.message](types/inference.message.md) – one turn of a conversation
* [inference.content_part](types/inference.content_part.md) – text or media
* [inference.media_ref](types/inference.media_ref.md) – where a part's bytes come from
* [inference.chunk](types/inference.chunk.md) – one delta of an answer
* [inference.usage](types/inference.usage.md) – what a request cost
