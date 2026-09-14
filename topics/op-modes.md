# Op modes & composition

An [Op](../core-definitions/op.md) reads input [Objects](../core-definitions/object.md)
from its [Channel](../core-definitions/channel.md) and writes results back. An `Op`
supports one or both of:

  - single mode — runs once; takes input via args and/or a single input `Object`;
    sends one result/error back.
  - batch mode — reads `Objects` from the `Channel` until EOS/EOF and runs the
    `Op` for each input, sending one result/error per input, in input order. A
    failed input does not end the batch; an input of an unexpected type is
    answered with an `error_message` in-band. An input the `Channel` cannot
    decode at all — an undecodable payload, an unknown `Object Type`, a
    corrupted frame — is answered with an `error_message` and ends the batch:
    the decoder is past the frame boundary, so no further input is readable.
    Results already sent for earlier inputs precede that `error_message` and
    stand. No terminator follows it. The reply stream otherwise mirrors the
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

## Control signals

An `Op`'s documentation can give an `Object` a signalling role through one of three
patterns. A client reads such an `Object` by the documentation of the `Op` that
exchanges it, not by its `Object Type` alone.

* readiness `ack` — an [`ack`](../primitive-types/ack.md) means completion by
  default: the `Op` has finished the work the `ack` answers. An `Op`'s documentation
  can instead state that its `ack` means readiness: the `Op` is set up and keeps the
  `Channel` open for the caller's further input. Closing the `Channel` after a
  readiness `ack` ends the `Op`, and the `Op` undoes what it holds open:
  [`objects.create`](../protocols/objects/ops/objects.create.md) discards the
  uncommitted data, [`apphost.bind`](../protocols/apphost/ops/apphost.bind.md)
  removes the bound handlers, and
  [`services.advertise`](../protocols/services/ops/services.advertise.md) withdraws
  the advertisement.
* typed final object — an `Op`'s documentation can name an `Object Type` that ends
  its output in place of an [`eos`](../primitive-types/eos.md). The named `Object` is
  the last one the `Op` sends and carries a value of its own; no `eos` follows it.
  [`user.sync_assets`](../protocols/user/ops/user.sync_assets.md) ends its output
  with a `uint64`, the next height to request. A client never blocks waiting for the
  named `Object` and treats EOF as a legitimate end of the response, as it does for
  `eos`.
* typed input terminator — an `Op`'s documentation can name an `Object Type` that
  ends the caller's input. The `Op` stops reading at the first input `Object` of that
  type. [`objects.create`](../protocols/objects/ops/objects.create.md) ends its input
  at a [`mod.objects.commit_msg`](../protocols/objects/types/mod.objects.commit_msg.md)
  and commits the written data.
  [`objects.echo`](../protocols/objects/ops/objects.echo.md) ends its input at the
  `Object Type` its `stop` argument names and does not echo that `Object`.

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
