# services.advertise

Open a binding between the calling provider app and its node for a fixed set of
services, and keep it open for as long as the provider serves them. Closing the
channel ends the binding.

The provider is the caller. There is no argument for it, so an app advertises
nothing but itself. The caller must hold
[`mod.auth.serve_apps_action`](../../auth/types/mod.auth.serve_apps_action.md).
The query is rejected, and a refused caller receives no bytes, when it arrives
over a [`Link`](../../../core-definitions/link.md), when the caller is the node
identity, or when the caller is not authorized.

`services` names every service of the binding, comma-separated. A name is
non-empty, contains no comma, has no leading or trailing whitespace, and fits a
`string8`; a list holds at least one name and no name twice. The set is fixed
for the life of the binding: changing it means closing the binding and
advertising the new set.

Admission is all-or-nothing. Each (provider, name) pair has at most one live
binding. If any pair of the set already belongs to a live binding, the
operation claims none of the set and leaves the existing binding untouched.
Closing a binding releases every pair it holds.

Advertising makes the services eligible for evaluation. It offers nothing to
any caller by itself, and it registers no operation.

## Arguments

* services (string8, required) – The service names of the binding, comma-separated.
* in (string8) – Input format.
* out (string8) – Output format.

## The binding

After the `ack` the channel carries, in both directions:

* node → provider: [`services.ask`](../types/services.ask.md). The node sends at
  most one ask per caller at a time, for one service and one caller.
* provider → node: [`services.answer`](../types/services.answer.md), one per
  ask, echoing its `RequestID`; and
  [`services.change`](../types/services.change.md) at any time.

The provider answers every ask; an ask the provider cannot evaluate is answered
with `Available` false. The node fails the binding on any other object, an
undecodable frame, an answer for the wrong service or provider, or a change with
`All` false and no callers. An answer that matches no outstanding ask is
ignored.

When the binding ends, every discovery stream that was shown one of its
offerings receives a [`services.removed`](../types/services.removed.md) for it.

## Returned objects

The operation returns one of:
* An `error_message` object if the list is invalid or a pair already belongs to a live binding, after which the channel closes.
* An `ack` object once the binding stands, followed by the binding exchange above.

The `ack` is a readiness `ack` — see
[Op modes & composition § Control signals](../../../topics/op-modes.md#control-signals).

## Examples

```shellsession
$ astral-query services.advertise -services player,bitcoin-wallet -out text
#[ack]
```
