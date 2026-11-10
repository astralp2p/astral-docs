# services.discover

The operation evaluates services for the caller and streams the offerings the
caller may see. `follow` keeps the stream open for later changes.

## Admission

`reach=local` (default) uses hosted providers. `reach=swarm` also queries every
other local swarm member for the app and merges their offerings. Swarm discovery
starts at the app's hosting node; `reach=swarm` over a
[Link](../../../core-definitions/link.md) is refused.

`services` names the services to discover. Without `services` the node
discovers every service its providers advertise, and every service of every
contributing member. `follow` requires `services`; a `follow` without
`services` is refused with `error_message`. Invalid names or `reach` values also
return `error_message`.

Admission refuses no caller for lack of permission. A direct query over a link
with `reach=local` is evaluated for the sending identity.
[Visibility](#visibility) decides which offerings reach the caller.

## Visibility

Every provider of a discovered service is asked, open and private alike, with
the caller's identity. The requesting node then filters each result where it
enters the caller's stream. A result of provider `P` for service `S` on node
`N` reaches the caller when:

* `P` is open on `N` and the caller is a swarm caller, or
* the caller holds
  [`mod.services.service_discovery_action`](../types/mod.services.service_discovery_action.md)
  for `S` on `N`.

A swarm caller is an app hosted on a node of the user's
[Local Swarm](../../../core-definitions/local-swarm.md), the user, or a node of
that swarm. An app is hosted on a swarm node when it issued an active
[`mod.nodes.relay_for_action`](../../nodes/types/mod.nodes.relay_for_action.md)
contract whose subject is that node. The node's own identity and the zero
identity are never swarm callers. Other identities, a friend's app or node
included, see only the offerings their permits allow.

`P` is open on `N` when its binding advertised `open: true` and no entry of
`N`'s [private list](../types/mod.services.private_list.md) covers it. A native
node service is open unless the private list covers it.

A filtered result is never sent: no update, no withdrawal and no removal. A
result that stops being visible to a follow removes a previously shown key with
[`services.removed`](../types/services.removed.md). A result that becomes
visible again arrives as a [`services.update`](../types/services.update.md).

When `services` is given, the stream starts with one
[`services.not_granted`](../types/services.not_granted.md) listing each
requested service the caller holds no discovery permit for on at least one
contributing node. Without such a service, or without `services`, no
`services.not_granted` is sent. The list depends only on the caller's permits,
never on providers.

## Discovery in an app's name

A hosting node pushes the app's relay contract to a swarm member, then queries
as itself with `for` naming the app and `tagged` set. The member requires:

* a query over a link with `reach=local` and a valid app identity in `for`;
* the sending node's
  [`mod.nodes.relay_for_action`](../../nodes/types/mod.nodes.relay_for_action.md)
  for that app;
* the sending node's discovery permission for every requested service there;
  without `services`, the sending node is a member of this node's local swarm.

Providers evaluate the named app. The member does not filter: it returns every
offering of its hosted providers, and the requesting node applies
[Visibility](#visibility). With `tagged`, the member sends each offering as a
[`services.tagged_update`](../types/services.tagged_update.md) carrying the
provider's effective visibility on the member, and re-sends a shown offering
when its visibility changes. Without `tagged`, the member sends plain
`services.update` objects. A query with `for` is never forwarded and never
receives `services.not_granted`. Invalid or unauthorized `for` requests return
`error_message` before evaluation.

A member refusing `tagged` as an unknown argument predates visibility. The
requesting node then queries it again without `tagged` and treats its results
as open.

## The initial attempt

Admission fixes the initial contributions: hosted providers for each
discovered service and, with `reach=swarm`, each other swarm member. Each
contribution is evaluated for the caller. Visible available offerings are
streamed as they arrive; initially unavailable offerings are omitted.

```text
Admission
  +-- refused --> error_message --> close
  +-- allowed --> [services.not_granted] --> offerings --> [services.incomplete] --> eos
                                                                              +-- follow=false --> close
                                                                              +-- follow=true ---> later changes
```

`eos` ends the initial attempt. A bare `eos` means all initial work completed,
including unavailable and filtered answers. With no contributions it arrives
immediately; `reach=swarm` with no other members behaves as local discovery.

[`services.incomplete`](../types/services.incomplete.md) precedes `eos` when
initial evaluation times out, a provider is lost, or a swarm member is
unreachable, refuses, times out, or reports incomplete work. It names affected
services and preserves received offerings; it is not discovery failure.
Without `services`, it names the affected services the node knows: those of
hosted providers, and those a member reported. A member lost before reporting
adds no name. Closing before `eos` is failure, not a successful empty result.

## Following

With `follow`, the stream stays open after either a complete or incomplete
initial attempt. It carries:

* [`services.update`](../types/services.update.md): a new or changed offering,
  including `Available: false` to withdraw a previously shown key;
* [`services.removed`](../types/services.removed.md): previously shown keys
  whose provider or contributing swarm member was lost, or that stopped being
  visible to the caller.

Each update replaces the complete offering. Slow readers receive the latest
value per key; a write exceeding the node's timeout closes the channel.

A lost swarm member is retried when a link appears, or with capped backoff
while the follow remains open. Recovered offerings arrive as updates.

A change to the private list re-evaluates the affected bindings for the
followers of their services.

## Arguments

* services (string8) – The service names to discover, comma-separated, at most 64. Names follow the rules of [`services.advertise`](services.advertise.md). Omitted, every advertised service is discovered.
* follow (bool) – If true, keep the channel open after the initial attempt. Requires `services`. Defaults to false.
* reach (string8) – `local` or `swarm`. Defaults to `local`.
* for (identity) – The app a swarm member discovers for. Only a node carrying a discovery sends it.
* tagged (bool) – If true, send offerings as `services.tagged_update`. Only a node carrying a discovery sends it, together with `for`. Defaults to false.
* in (string8) – Input format.
* out (string8) – Output format.

## Returned objects

* `error_message`, then close: invalid arguments, `follow` without `services`,
  or a refused `for` request.
* An optional `services.not_granted`, `services.update` objects (or
  `services.tagged_update` objects with `tagged`), an optional
  `services.incomplete`, then `eos`; with `follow`, later updates and removals
  until closure. Provider loss can also remove a shown offering before `eos`.

## Examples

```shellsession
$ astral-query services.discover -services player -out json
{"Type":"services.update","Object":{"Available":true,"Name":"player","ProviderID":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f","Info":[{"Type":"services.operations_list","Object":{"Operations":["player.play","player.pause"]}}]}}
{"Type":"eos","Object":null}
```

A swarm app without a permit for `player` sees open players only:

```shellsession
$ astral-query services.discover -services player -out json
{"Type":"services.not_granted","Object":{"Services":["player"]}}
{"Type":"services.update","Object":{"Available":true,"Name":"player","ProviderID":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f","Info":null}}
{"Type":"eos","Object":null}
```

Every service the caller may see:

```shellsession
$ astral-query services.discover -out json
{"Type":"services.update","Object":{"Available":true,"Name":"player","ProviderID":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f","Info":null}}
{"Type":"services.update","Object":{"Available":true,"Name":"gateway","ProviderID":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Info":null}}
{"Type":"eos","Object":null}
```

Players across the swarm, one member out of reach:

```shellsession
$ astral-query services.discover -services player -reach swarm -out json
{"Type":"services.update","Object":{"Available":true,"Name":"player","ProviderID":"02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f","Info":null}}
{"Type":"services.incomplete","Object":{"Services":["player"]}}
{"Type":"eos","Object":null}
```
