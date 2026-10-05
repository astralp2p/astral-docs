# Services

* A `Service` is a capability an [`App`](../core-definitions/app.md) offers to other `Apps`, under a
  free-text name chosen by whoever defines its contract: `player`, `bitcoin-wallet`,
  `contacts-backend`. A `Service` name is not an [`Op`](../core-definitions/op.md) namespace and
  carries no permission of its own.
* The [`services`](../protocols/services/README.md) protocol answers one question for an `App`:
  which providers offer it which services, and what they offer it. A provider is an `App` that
  advertises a `Service`, or the [`Node`](../core-definitions/node.md) itself for a `Service` the
  `Node` offers, such as `nat` or `gateway`.
* An offering is caller-specific. A provider evaluates every caller on its own and answers with a
  complete [`services.update`](../protocols/services/types/services.update.md) for that caller: two
  `Apps` asking the same provider for the same `Service` can be offered different
  [`Ops`](../core-definitions/op.md), or nothing.
* An offering is keyed by its provider `Identity` and its `Service` name
  ([`services.offering_key`](../protocols/services/types/services.offering_key.md)). Its `Info`
  bundle carries what the contract defines, typically a
  [`services.operations_list`](../protocols/services/types/services.operations_list.md) naming
  the `Ops` the caller may address to the provider.
* An offering grants nothing. Every `Op` it lists checks the caller's permission when it runs.
* A `Node` caches no offering. Every view a consumer receives is a fresh answer from the provider
  for that consumer.

```text
 provider app                       node                           consumer app
 ────────────                       ────                           ────────────
 services.advertise player ───────► binding: (provider, player)
                                                       ◄────────── services.discover player
 ◄──────────── services.ask (caller = consumer, player)
 services.answer (available, ops) ─►
                                    services.update ────────────► offering: provider, player, ops
                                                                   eos (initial attempt done)
 services.change (callers) ────────► re-asks the consumer ...  ──► newer services.update
```

## Advertising a service

* An `App` provisions itself with `apphost.register`, which grants
  [`mod.auth.serve_apps_action`](../protocols/auth/types/mod.auth.serve_apps_action.md) — the
  permission to advertise itself. A provider advertises no `Identity` but its own: the
  [`services.advertise`](../protocols/services/ops/services.advertise.md) `Op` takes the provider
  from the caller.
* `services.advertise` names a fixed set of `Services`, comma-separated, at most 64. The `Node`
  claims every (provider, name) pair of the set, or none: a pair that a live binding already holds
  refuses the whole set with an `error_message`. On success the `Node` answers `ack`, and the
  channel stays open as the binding.
* While the binding is open:
  * the `Node` sends [`services.ask`](../protocols/services/types/services.ask.md) — evaluate one
    `Service` for one caller. It sends at most one ask per caller at a time.
  * the provider answers each ask with
    [`services.answer`](../protocols/services/types/services.answer.md), echoing its `RequestID`
    and carrying the caller's complete offering. `Available` false is an answer: nothing for this
    caller.
  * the provider sends [`services.change`](../protocols/services/types/services.change.md) when the
    offerings of some callers, or of all, may have changed. The `Node` re-asks every caller that
    follows a `Service` of the binding; the provider never pushes an offering on its own.
* Closing the channel ends the binding. Every consumer that was shown one of its offerings receives
  a [`services.removed`](../protocols/services/types/services.removed.md) for it. Re-advertising
  opens a new binding, evaluated from scratch.
* The binding fails on anything else the provider sends: another object, an undecodable frame, an
  answer for the wrong `Service` or provider, or a change selecting no caller.
* `services.advertise` is local-only. A query arriving over a [`Link`](../core-definitions/link.md)
  is rejected, and so is the `Node`'s own `Identity`: an `App` advertises on the `Node` that hosts
  it.

A Go provider built on astral-go advertises from its app's registration and answers each caller:

```go
p := servicescli.NewProvider(map[string]servicescli.OfferingFunc{
	"player": func(ctx *astral.Context, caller *astral.Identity) (*services.Update, error) {
		info := astral.NewBundle()
		info.Append(&services.OperationsList{Operations: []astral.String8{"player.play", "player.pause"}})
		return &services.Update{Available: true, Info: info}, nil
	},
})
apps.Serve(ctx, router, apps.WithServices(p)) // advertises on every (re)registration

p.Change(caller) // this caller's offering may have changed
p.ChangeAll()    // every following caller's
```

An astral-js provider does the same on a connected host:

```ts
const binding = await advertise(host, {
  'chat-room': (caller) => (members.has(caller) ? { info: [] } : null), // null: nothing for this caller
});
binding.change(bob);
```

* A `Node` offers its own `Services` through the same machinery: a module registers names and an
  evaluator inside the `Node`, and its offerings carry the `Node` `Identity` as `ProviderID`.

## Discovering services

* An `App` asks its own `Node` with
  [`services.discover`](../protocols/services/ops/services.discover.md), naming the `Services` it
  wants, at most 64. There is no "discover everything".
* On admission the `Node` fixes the providers that hold a requested `Service`, asks each of them
  once for the caller, and streams each offering as it arrives. A provider offering nothing to the
  caller is not shown.
* An `eos` ends the initial attempt:
  * a bare `eos` — every provider answered, including those that offered nothing;
  * [`services.incomplete`](../protocols/services/types/services.incomplete.md) then `eos` — some
    provider did not answer within the `Node`'s budget; the object names the affected `Services`,
    never a provider or a `Node`;
  * a requested `Service` with no provider owes nothing: the `eos` arrives at once.
* Without `follow` the channel closes after the `eos`; a channel that closes before the `eos` is a
  failure, not an empty result. With `follow` it stays open and carries a new `services.update`
  whenever an offering changes, a provider of a requested `Service` starts, or a shown offering is
  withdrawn (`Available` false), and a `services.removed` when a provider is lost.
* A slow consumer receives the latest offering of each key, not every intermediate one. A consumer
  that stops reading is disconnected.

```shellsession
$ astral-query services.discover -services player -out json
{"Type":"services.update","Object":{"Available":true,"Name":"player","ProviderID":"02bef8…","Info":[…]}}
{"Type":"eos","Object":null}
```

```go
w, _ := servicescli.Watch(ctx, []string{"player"}) // follow, keeping the current set
<-w.Initial()
for range w.Changed() {
	render(w.Offerings())
}
```

### Who may discover

* Discovering a `Service` requires
  [`mod.services.service_discovery_action`](../protocols/services/types/mod.services.service_discovery_action.md)
  for that `Service` on each contributing `Node`. A request naming one `Service` the caller may not
  discover is refused with an `error_message` before any provider is asked; a request is never
  narrowed.
* The [`User`](../core-definitions/user.md) holds the action for every `Service`. A member of the
  [`Local Swarm`](../core-definitions/local-swarm.md) holds it for every `Service` on every other
  member. The `Node`'s own `Identity` holds none.
* Any other `App` holds it through a grant scoped by a
  [`mod.services.discovery_scope`](../protocols/services/types/mod.services.discovery_scope.md),
  which pairs `Services` with the `Nodes` they may be discovered on. An unconstrained permit covers
  nothing, so an `App` cannot grant itself discovery at registration. The `User` grants it once, on
  the `Node` the `App` asks:

```shellsession
$ echo '{"Type":"bundle","Object":[{"Type":"mod.services.discovery_scope","Object":{"Rules":[{"Services":["player"]}]}}]}' \
    | astral-query apphost.grant -identity <app> -action mod.services.service_discovery_action -constrained true -in json
```

A rule with no `Nodes` allows its `Services` on every `Node` the discovery reaches.

## Discovering across the swarm

* `reach=swarm` makes the `Node` carry the discovery to every member of its `Local Swarm`, in the
  `App`'s name, and merge their offerings into the one stream. `reach` defaults to `local`, the
  providers the `Node` hosts.
* The `Node` first checks the `App`'s permission for every requested `Service` on every member.
  It then pushes the `App`'s relay `Contract` to each member and queries it as itself, naming the
  `App` in `for`.
* The member admits the query when the asking `Node` may relay for the `App`
  ([`mod.nodes.relay_for_action`](../protocols/nodes/types/mod.nodes.relay_for_action.md)) and may
  discover the `Services` there. It asks its providers for the `App` — never for the asking
  `Node` — and answers from the providers it hosts. A query with `for` is never carried further.
* Each member counts as one contribution to the initial attempt. A member that cannot be reached,
  refuses, does not finish within the budget, or reports its own `services.incomplete` makes the
  outcome incomplete for the requested `Services`.
* A member lost during a follow has its shown offerings removed. The `Node` asks it again when a
  `Link` to it comes up, and otherwise retries with a capped backoff while the follow is open.

```ts
const w = await watch(host, ['player'], { reach: 'swarm' }); // every player on the user's devices
```

## Using an offering

* An offering's `ProviderID` is the `Target` of the provider's `Ops`. The consumer addresses them
  like any other query: `<ProviderID>:player.play`.
* A provider on the consumer's own `Node` is reached directly. A provider `App` on another `Node`
  is reached through its host, by the relay `Contract` the provider signed with that host — see
  [`App Routing`](app-routing.md). A `Node` learns its members' relay `Contracts` when a `Link` to
  each member first comes up; an `App` registered while the two `Nodes` are already linked becomes
  reachable from the other at the next first `Link`.
* A `Service` the `Node` offers itself is addressed to the `Node` `Identity`, over the `Link`.

## Lifetimes and limits

* `Services` state lives as long as the `Node` process. A restart ends every binding and every
  discovery stream; providers advertise again and consumers discover again.
* A (provider, name) pair has at most one live binding. A provider restarting before its `Node`
  has noticed the old binding closing is refused as already advertised, and retries.
* A `Service` name is non-empty, holds no comma and no leading or trailing whitespace, and fits a
  `string8`; one call names at most 64.
* Budgets and timeouts are the `Node`'s own. astrald waits 5 s for an initial attempt, 10 s for one
  answer, and 10 s for a write to a consumer; the values are not part of the protocol.
