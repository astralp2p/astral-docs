# Op modes & composition

An [Op](../core-definitions/op.md) reads input [Objects](../core-definitions/object.md)
from its [Channel](../core-definitions/channel.md) and writes results back. An `Op`
supports one or both of:

  - single mode — runs once; takes input via args and/or a single input `Object`;
    sends one result/error back.
  - batch mode — reads `Objects` from the `Channel` until EOS/EOF and runs the
    `Op` for each input, sending one result/error per input, in input order. A
    failed input does not end the batch; an input of an unexpected type is
    answered with an `error_message` in-band. The reply stream mirrors the
    input stream's terminator: an explicit EOS input is answered with a final
    EOS; a stream ended by EOF is not.

## Reading a response

* EOF always ends a response. A `Channel` that closes has delivered everything
  the `Op` will send.
* An `EOS` is a terminator an `Op` may send in addition. Batch mode mirrors the
  input terminator, as above. In single mode, and for long-lived streams, whether
  an `EOS` arrives belongs to the individual `Op`'s contract and is stated in its
  documentation.
* A client must never block waiting for an `EOS`. It consumes one when present
  and treats EOF as a legitimate end of the response in every case. A client that
  waits for a terminator the `Op` does not send hangs until the connection drops.

## Composing single-mode ops

* A single-mode `Op` is a filter: one input `Object` produces one result `Object`.
  Two `Ops` compose when the upstream `Op`'s returned [`Object Type`](../core-definitions/object-type.md)
  is the `Object Type` the downstream `Op` reads — each `Op`'s documentation states
  both, so they read as a connector.
* Composition feeds the upstream result as the downstream input. Over
  [astral-query](../tools/astral-query.md) this is a shell pipe; over the
  [WebSocket](ws-transport.md) or [HTTP](http-transport.md) surfaces it is the
  `Channel` byte stream. Both sides must agree on an encoding — see
  [Binary](binary-encoding.md), [JSON](json-encoding.md), [Text](text-encoding.md).
* Composition carries no atomicity guarantee, and an `Op` reports failure in-band
  as an [`error_message`](../primitive-types/error_message.md) `Object` rather than out of band: a failed stage emits an
  `Object` of the wrong type into the stream instead of halting the pipeline. Do
  not compose `Ops` whose effects must apply together.
* batch mode is fan-out within a single `Op` (one stream of inputs, one result
  each), not a substitute for composing different `Ops`.
