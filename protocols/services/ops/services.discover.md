# services.discover

Evaluate the requested services for the caller and stream the offerings. With
`follow` the stream stays open and delivers later changes.

An app asks only its own node. With `reach=local`, the default, the node answers
from the providers it hosts. With `reach=swarm` the node also carries the
discovery to every member of its local swarm, in the app's name, and merges
their offerings into the one stream.

## Admission

The caller must hold
[`mod.services.service_discovery_action`](../types/mod.services.service_discovery_action.md)
for every requested service on every contributing node: this node, and with
`reach=swarm` every swarm member. A request naming any service on any node the
caller may not discover is refused with an `error_message` before any provider
is evaluated. A request is never narrowed.

A query arriving over a [`Link`](../../../core-definitions/link.md) is checked
the same way, for the identity that sent it.

A `reach` other than `local` or `swarm` is refused with an `error_message`.

## Discovery in an app's name

A node that carries a discovery to a swarm member queries the member as itself
and names the app in `for`. The member admits the query only when:

* it arrives over a `Link`;
* the sending node holds
  [`mod.nodes.relay_for_action`](../../nodes/types/mod.nodes.relay_for_action.md)
  for the app, which the sending node shows by pushing the app's relay contract
  first;
* the sending node holds `mod.services.service_discovery_action` for every
  requested service on the member;
* `reach` is `local`.

The member then evaluates its providers for the app, not for the sending node,
and answers from the providers it hosts. A query with `for` is never carried
further.

## The initial attempt

On admission the node fixes the set of contributions: each provider it hosts
that offers a requested service, and with `reach=swarm` each swarm member. It
asks each of them once for the caller and streams each offering as it arrives.
A provider that offers nothing to the caller is not shown.

An `eos` ends the initial attempt. If every contribution answered, the `eos`
arrives alone. A [`services.incomplete`](../types/services.incomplete.md)
naming the affected services arrives immediately before the `eos` when a
provider did not answer before the node's budget expired or its binding closed,
or when a swarm member could not be reached, refused the query, did not finish
its own initial attempt in time, or reported its own `services.incomplete`. A
requested service with no contribution owes no work: an attempt with nothing to
ask ends at once with a bare `eos`. With `reach=swarm` and no other swarm member
the result is the local one.

Without `follow` the channel closes after the `eos`. A channel that closes
before the `eos` reports a failure, not an empty result.

## Following

With `follow` the channel stays open after the `eos`, whether the initial
attempt was complete or not, and carries:

* a [`services.update`](../types/services.update.md) whenever an offering for
  the caller changes, a provider of a requested service starts, or a shown
  offering is withdrawn (`Available` false);
* a [`services.removed`](../types/services.removed.md) when the provider of
  shown offerings is lost, or the swarm member that contributed them is lost.

Each update is the complete current offering. A slow reader receives the latest
offering of each key, not every intermediate one.

A lost swarm member is asked again when a link to it is created, and otherwise
retried with a capped backoff, for as long as the follow is open. Its offerings
then arrive as updates.

## Arguments

* services (string8, required) – The service names to discover, comma-separated, at most 64. Names follow the rules of [`services.advertise`](services.advertise.md).
* follow (bool) – If true, keep the channel open after the initial attempt. Defaults to false.
* reach (string8) – `local` or `swarm`. Defaults to `local`.
* for (identity) – The app a swarm member discovers for. Only a node carrying a discovery sends it.
* in (string8) – Input format.
* out (string8) – Output format.

## Returned objects

The operation returns one of:
* An `error_message` object if the list or `reach` is invalid, or a requested service is not permitted.
* A stream of `services.update` objects, an optional `services.incomplete`, and an `eos`; with `follow`, further `services.update` and `services.removed` objects until the channel closes.

## Examples

```shellsession
$ astral-query services.discover -services player -out json
{"Type":"services.update","Object":{"Available":true,"Name":"player","ProviderID":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f","Info":[{"Type":"services.operations_list","Object":{"Operations":["player.play","player.pause"]}}]}}
{"Type":"eos","Object":null}
```

Players across the swarm, one member out of reach:

```shellsession
$ astral-query services.discover -services player -reach swarm -out json
{"Type":"services.update","Object":{"Available":true,"Name":"player","ProviderID":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f","Info":null}}
{"Type":"services.incomplete","Object":{"Services":["player"]}}
{"Type":"eos","Object":null}
```
