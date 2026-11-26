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

### Authority changes

A follow applies the caller's current authority for as long as it is open. The
node re-checks every follow of a caller after any of these changes is
recorded:

* a contract indexed whose issuer or subject is the caller, or a contract
  withdrawn on the node;
* a [`mod.user.swarm_member_joined`](../../user/types/mod.user.swarm_member_joined.md)
  or [`mod.user.swarm_member_left`](../../user/types/mod.user.swarm_member_left.md)
  event, which re-checks every follow.

The re-check runs after the change is recorded, never inside the operation that
records it. It answers the swarm caller question and every permit question
again. An offering the caller may no longer see is removed with
`services.removed`, cause `hidden`, and later results of that provider are
filtered. An offering of a hosted provider the caller may now see is evaluated
again and arrives as a `services.update`. When the caller may now see more, a
follow with `reach=swarm` restarts the carry to each member; an offering shown
before and after the restart stays shown without a removal.

A re-check that changes the `services.not_granted` list sends a new
`services.not_granted` with the current list. An empty list means the caller
holds a permit for every requested service on every contributing node. A
one-shot discovery keeps the authority it was admitted with.

## Discovery in an app's name

A hosting node pushes the app's relay contract to a swarm member, then queries
as itself with `for` naming the app and `tagged` set. The member requires:

* a query over a link with `reach=local` and a valid app identity in `for`;
* the sending node's
  [`mod.nodes.relay_for_action`](../../nodes/types/mod.nodes.relay_for_action.md)
  for that app;
* the sending node is a member of this node's local swarm.

Providers evaluate the named app. The member filters as the app: an open
offering passes, and a private one passes only when the app holds a discovery
permit for its service on the member, walked through the app's own contract
chain. The member re-applies the app's permits after a change of its
authority. The requesting node then applies [Visibility](#visibility) for its
caller. With `tagged`, the member sends each offering as a
[`services.tagged_update`](../types/services.tagged_update.md) carrying the
provider's effective visibility on the member, and re-sends a shown offering
when its visibility changes. Without `tagged`, the member sends plain
`services.update` objects. A query with `for` is never forwarded and never
receives `services.not_granted`. Invalid or unauthorized `for` requests return
`error_message` before evaluation.

The member re-checks an open stream with `for` after the same changes as a
follow, recorded for the app or for the sending node. When the sending node no
longer holds the relay right for the app, or is no longer a member of the
local swarm,
the member closes the stream without an error object.
A sending node that leaves the local swarm has its streams with `for` closed
when the `mod.user.swarm_member_left` event arrives, whether or not the link
stays up. The sending node's carry retries and is refused at admission.

A member that predates visibility ignores `tagged` and sends plain
`services.update` objects. The requesting node treats an untagged offering
from a member as open.

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
adds no name; when no affected service is known, `Services` is empty. Closing before `eos` is failure, not a successful empty result.

## Following

With `follow`, the stream stays open after either a complete or incomplete
initial attempt. It carries:

* [`services.update`](../types/services.update.md): a new or changed offering,
  including `Available: false` to withdraw a previously shown key;
* [`services.removed`](../types/services.removed.md): previously shown keys
  whose provider or contributing swarm member was lost, or that stopped being
  visible to the caller, with the cause of the removal;
* [`services.not_granted`](../types/services.not_granted.md): the current list
  after an [authority change](#authority-changes) altered it.

Each update replaces the complete offering. Slow readers receive the latest
value per key; a write exceeding the node's timeout closes the channel.

A lost swarm member is retried when a link appears, or with capped backoff
while the follow remains open. Its shown offerings are removed with cause
`member_lost`. Recovered offerings arrive as updates.

A follow with `reach=swarm` tracks the local swarm member set while it is open:

* A node that joins the swarm becomes a contributing member. Its offerings
  arrive as `services.update`. A member that joins before `eos` adds no initial
  work: `eos` neither waits for it nor reports it in `services.incomplete`.
* A member that leaves the swarm stops contributing. Its shown offerings are
  removed with `services.removed` and cause `member_left`, and the node stops
  asking it for the follow.
  A member that leaves before reporting its initial outcome counts as lost.
  A member leaves when it is expelled, when its last membership contract
  expires, or when the active contract changes or is cleared.

Membership changes reach the follow through the user module's
[`mod.user.swarm_member_joined`](../../user/types/mod.user.swarm_member_joined.md)
and [`mod.user.swarm_member_left`](../../user/types/mod.user.swarm_member_left.md)
events. A one-shot discovery keeps the members it was admitted with.

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
  `services.incomplete`, then `eos`; with `follow`, later updates, removals and
  `services.not_granted` lists until closure. Provider loss or an authority
  change can also remove a shown offering, and an authority change can send a
  new `services.not_granted`, before `eos`.

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
