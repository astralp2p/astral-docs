# services.discover

The operation evaluates named services for the caller and streams their
offerings. `follow` keeps the stream open for later changes.

## Admission

`reach=local` (default) uses hosted providers. `reach=swarm` also queries every
other local swarm member for the app and merges their offerings. Swarm discovery
starts at the app's hosting node; `reach=swarm` over a
[Link](../../../core-definitions/link.md) is refused.

The caller must hold
[`mod.services.service_discovery_action`](../types/mod.services.service_discovery_action.md)
for every requested service on every contributing node. One denied pair refuses
the entire request with `error_message`, before any provider is evaluated.
Invalid names or `reach` values also return `error_message`.

A direct query over a link with `reach=local` checks the sending identity.
Permission refusal differs from a provider's `Available: false` answer; see
[consumer outcomes](../../../topics/services.md#reading-the-outcome).

## Discovery in an app's name

A hosting node pushes the app's relay contract to a swarm member, then queries
as itself with `for` naming the app. The member requires:

* a query over a link with `reach=local` and a valid app identity in `for`;
* the sending node's
  [`mod.nodes.relay_for_action`](../../nodes/types/mod.nodes.relay_for_action.md)
  for that app;
* the sending node's discovery permission for every requested service there.

Providers evaluate the named app. The member returns only its hosted providers'
offerings; a query with `for` is never forwarded. Invalid or unauthorized `for`
requests return `error_message` before evaluation.

## The initial attempt

Admission fixes the initial contributions: hosted providers for each requested
service and, with `reach=swarm`, each other swarm member. Each contribution is
evaluated for the caller. Available offerings are streamed as they arrive;
initially unavailable offerings are omitted.

```text
Admission
  +-- refused --> error_message --> close
  +-- allowed --> offerings --> [services.incomplete] --> eos
                                                          +-- follow=false --> close
                                                          +-- follow=true ---> later changes
```

`eos` ends the initial attempt. A bare `eos` means all initial work completed,
including unavailable answers. With no contributions it arrives immediately;
`reach=swarm` with no other members behaves as local discovery.

[`services.incomplete`](../types/services.incomplete.md) precedes `eos` when
initial evaluation times out, a provider is lost, or a swarm member is
unreachable, refuses, times out, or reports incomplete work. It names affected
services and preserves received offerings; it is not discovery failure.
Closing before `eos` is failure, not a successful empty result.

## Following

With `follow`, the stream stays open after either a complete or incomplete
initial attempt. It carries:

* [`services.update`](../types/services.update.md): a new or changed offering,
  including `Available: false` to withdraw a previously shown key;
* [`services.removed`](../types/services.removed.md): previously shown keys
  whose provider or contributing swarm member was lost.

Each update replaces the complete offering. Slow readers receive the latest
value per key; a write exceeding the node's timeout closes the channel.

A lost swarm member is retried when a link appears, or with capped backoff
while the follow remains open. Recovered offerings arrive as updates.

## Arguments

* services (string8, required) – The service names to discover, comma-separated, at most 64. Names follow the rules of [`services.advertise`](services.advertise.md).
* follow (bool) – If true, keep the channel open after the initial attempt. Defaults to false.
* reach (string8) – `local` or `swarm`. Defaults to `local`.
* for (identity) – The app a swarm member discovers for. Only a node carrying a discovery sends it.
* in (string8) – Input format.
* out (string8) – Output format.

## Returned objects

* `error_message`, then close: invalid arguments or denied admission.
* `services.update` objects, optional `services.incomplete`, then `eos`;
  with `follow`, later updates and removals until closure. Provider loss can
  also remove a shown offering before `eos`.

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
