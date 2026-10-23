# services.advertise

The operation binds the calling provider app to a fixed set of service names
on its hosting node. The channel remains open for the binding's lifetime;
closing it releases all names. Advertising registers no operation and offers
nothing until a provider answers an evaluation request.

## Admission

The caller is the provider and must hold
[`mod.auth.serve_apps_action`](../../auth/types/mod.auth.serve_apps_action.md).
A query over a [Link](../../../core-definitions/link.md), the node identity,
or a caller without that permit is rejected with code 1 and no payload.

[`apphost.register`](../../apphost/ops/apphost.register.md) returns an app token
and requests the advertising grant, subject to registration policy. The node's
token authenticates as the rejected node identity. Under default apphost
settings, a token-less session receives `error_msg{denied}` before routing.
See [Session Identity](../../../topics/session-identity.md).

`services` contains 1–64 distinct, comma-separated names. Each name is non-empty,
contains no comma or surrounding whitespace, and fits `string8`. The set remains
fixed until the binding closes.

Admission claims every `(provider, name)` pair or none. A pair held by another
live binding refuses the entire set and leaves the existing binding untouched.

## Arguments

* services (string8, required) – The service names of the binding, comma-separated.
* in (string8) – Input format.
* out (string8) – Output format.

## The binding

The initial `ack` confirms readiness. The open channel then carries:

| Direction | Object | Rule |
|-----------|--------|------|
| node → provider | [`services.ask`](../types/services.ask.md) | One service and caller; at most one outstanding ask per binding and caller. |
| provider → node | [`services.answer`](../types/services.answer.md) | Echo `RequestID`; `Update.Name` must equal the asked `Service`. |
| provider → node | [`services.change`](../types/services.change.md) | Select callers for re-evaluation of followed services. |

Every ask requires an answer. `Available: false` means nothing is offered to
that caller and keeps the binding open. The node supplies `Update.ProviderID`.

For an outstanding ask, a missing `Update`, mismatched `Update.Name`, or a
non-empty `ProviderID` different from the binding's provider fails the binding.
An undecodable frame, unexpected object, or change with `All: false` and no
callers also fails it. Closure removes shown offerings through
[`services.removed`](../types/services.removed.md) and marks unresolved initial
evaluations in [`services.incomplete`](../types/services.incomplete.md).

The node retires unanswered asks at its request timeout. An answer with no
matching outstanding `RequestID`, including a late answer, is ignored.

## Returned objects

* `error_message`, then close: invalid names or an already-bound pair.
* `ack`, then the binding exchange: successful admission. This is a
  [readiness ack](../../../topics/op-modes.md#control-signals).

## Examples

```shellsession
$ astral-query services.advertise -services player,bitcoin-wallet -out text
#[ack]
```
