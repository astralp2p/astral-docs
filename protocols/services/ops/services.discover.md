# services.discover

Evaluate the requested services for the caller and stream the offerings. With
`follow` the stream stays open and delivers later changes.

The caller must hold
[`mod.services.service_discovery_action`](../types/mod.services.service_discovery_action.md)
for every requested service on this node. A request naming any service the
caller may not discover is refused with an `error_message` before any provider
is evaluated. The query is rejected when it arrives over a
[`Link`](../../../core-definitions/link.md): discovery is local.

## The initial attempt

On admission the node fixes the set of providers that offer a requested service,
asks each of them once for the caller, and streams each offering as it arrives.
A provider that offers nothing to the caller is not shown.

An `eos` ends the initial attempt. If every provider asked answered, the `eos`
arrives alone. If some did not answer before the node's budget expired, or its
binding closed, a [`services.incomplete`](../types/services.incomplete.md)
naming the affected services arrives immediately before the `eos`. A requested
service with no provider owes no work: an attempt where no service has a
provider ends at once with a bare `eos`.

Without `follow` the channel closes after the `eos`. A channel that closes
before the `eos` reports a failure, not an empty result.

## Following

With `follow` the channel stays open after the `eos`, whether the initial
attempt was complete or not, and carries:

* a [`services.update`](../types/services.update.md) whenever an offering for
  the caller changes, a provider of a requested service starts, or a shown
  offering is withdrawn (`Available` false);
* a [`services.removed`](../types/services.removed.md) when the provider of
  shown offerings is lost.

Each update is the complete current offering. A slow reader receives the latest
offering of each key, not every intermediate one.

## Arguments

* services (string8, required) – The service names to discover, comma-separated. Names follow the rules of [`services.advertise`](services.advertise.md).
* follow (bool) – If true, keep the channel open after the initial attempt. Defaults to false.
* in (string8) – Input format.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object if the list is invalid or a requested service is not permitted.
* A stream of `services.update` objects, an optional `services.incomplete`, and an `eos`; with `follow`, further `services.update` and `services.removed` objects until the channel closes.

## Examples

```shellsession
$ astral-query services.discover -services player -out json
{"Type":"services.update","Object":{"Available":true,"Name":"player","ProviderID":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f","Info":[{"Type":"services.operations_list","Object":{"Operations":["player.play","player.pause"]}}]}}
{"Type":"eos","Object":null}
```

A provider that did not answer in time:

```shellsession
$ astral-query services.discover -services player -out json
{"Type":"services.incomplete","Object":{"Services":["player"]}}
{"Type":"eos","Object":null}
```
