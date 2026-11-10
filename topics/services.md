# Services

The [`services`](../protocols/services/README.md) protocol discovers what providers
offer a caller. A provider is an [App](../core-definitions/app.md), or a
[Node](../core-definitions/node.md) offering a native service such as `nat` or
`gateway`. A service name identifies a contract, such as `player`; it need not
match an operation namespace.

An [offering](../protocols/services/types/services.update.md) is a complete,
caller-specific answer keyed by `(ProviderID, Name)`. Its `Info` bundle carries
service-defined terms, typically an
[operations list](../protocols/services/types/services.operations_list.md).
Different callers can receive different offerings. Discovery evaluates providers
afresh; an offering grants no permission to run its operations.

```text
Provider app                  Node                         Consumer app
     |-- advertise player ---->|                                |
     |<-- ack -----------------|<-- discover player ------------|
     |<-- ask(caller, player) --|                                |
     |-- answer(update) ------>|-- update, if available -------->|
     |                         |-- eos ------------------------>|
     |                         |                initial attempt ends
     |-- change(callers) ----->|                with follow:
     |<-- ask(caller, player) --|                                |
     |-- answer(update) ------>|-- update --------------------->|
```

## Advertising a service

[`services.advertise`](../protocols/services/ops/services.advertise.md) binds the
calling app to a fixed set of names on its hosting node. Admission claims every
`(provider, name)` pair or none; an existing binding for any pair refuses the
whole set. The initial `ack` confirms readiness.

### Provider rules

* **Identity and permission:** the caller must be an app identity holding
  [`mod.auth.serve_apps_action`](../protocols/auth/types/mod.auth.serve_apps_action.md).
  [`apphost.register`](../protocols/apphost/ops/apphost.register.md) requests that
  grant; registration policy decides whether to issue it. A query over a link is
  answered `origin not allowed: network`; the node identity, or a caller without
  the permit, is answered `not permitted`. With default apphost settings, a token-less session is denied
  before routing. See [Session Identity](session-identity.md).
* **Answer correlation:** each [`services.ask`](../protocols/services/types/services.ask.md)
  names one caller and service. The provider's
  [`services.answer`](../protocols/services/types/services.answer.md) echoes
  `RequestID`; `Update.Name` must equal the asked `Service`. A mismatched name
  fails the binding, removes its shown offerings, and marks its unresolved
  initial evaluations incomplete. The node supplies `ProviderID`.
* **Unavailable is an answer:** `Available: false` means nothing is offered to
  this caller. The binding stays open.
* **Changes trigger evaluation:** [`services.change`](../protocols/services/types/services.change.md)
  selects callers whose followed services need re-evaluation. The node sends
  new asks; providers do not push unsolicited offerings.
* **Visibility:** `open` (default true) lets every swarm caller find the
  binding without a permit. A provider whose existence is sensitive, such as a
  wallet, advertises with `open: false`; only callers holding a discovery
  permit then find it. See [Who sees an offering](#who-sees-an-offering).

Closing the binding releases its names and removes its shown offerings.
Re-advertising starts fresh. The
[operation reference](../protocols/services/ops/services.advertise.md#the-binding)
defines malformed-message and timeout handling. Native node services use an
internal evaluator; they do not call `services.advertise` as the node identity.

A Go provider uses its app registration; the SDK constructs the answer envelope:

```go
p := servicescli.NewProvider(map[string]servicescli.OfferingFunc{
	"player": func(ctx *astral.Context, caller *astral.Identity) (*services.Update, error) {
		info := astral.NewBundle()
		info.Append(&services.OperationsList{Operations: []astral.String8{"player.play", "player.pause"}})
		return &services.Update{Available: true, Info: info}, nil
	},
})
apps.Serve(ctx, router, apps.WithServices(p)) // advertises on every (re)registration

p.Change(caller) // this caller's offering may have changed p.ChangeAll()    //
every following caller's ```

An astral-js provider evaluates callers on a connected host:

```ts
const binding = await advertise(host, {
  'chat-room': (caller) => (members.has(caller) ? { info: [] } : null), // null: unavailable
});
binding.change(bob);
```

## Discovering services

[`services.discover`](../protocols/services/ops/services.discover.md) requests
services from the app's node. With `services` it discovers the named services;
without it, every advertised service. Admission fixes the initial contributions:
local providers for the discovered services, plus swarm members when
`reach=swarm`. The node evaluates them for the caller and streams the visible
available offerings as they arrive. A `follow` requires `services`.

An `eos` ends the initial attempt. Without `follow`, the channel then closes.
With `follow`, it stays open for updated offerings, withdrawals, new providers,
and provider removals. Updates replace the complete offering for a key; slow
readers receive the latest value, not every intermediate value. A write timeout
disconnects the consumer.

```go
w, _ := servicescli.Watch(ctx, []string{"player"}) // follow, keeping the current set
<-w.Initial()
for range w.Changed() {
	render(w.Offerings())
}
```

### Reading the outcome

| Signal | Meaning and consumer action |
|--------|-----------------------------|
| [`services.not_granted`](../protocols/services/types/services.not_granted.md) | The caller holds no permit for the listed services on some contributing node; private offerings there are filtered. Open offerings still arrive. Ask for a grant to see more. |
| `services.update`, `Available: true` | Add or replace the offering for `(ProviderID, Name)`. |
| `services.update`, `Available: false` | The provider withdraws a previously shown offering; remove that key. An initially unavailable offering is not sent. |
| [`services.removed`](../protocols/services/types/services.removed.md) | A provider or contributing swarm member was lost, or the offering stopped being visible; remove the listed keys. |
| `eos` without `services.incomplete` | Initial evaluation completed, including unavailable and filtered answers. No offerings can mean no providers, no available answers, or no visible ones. |
| [`services.incomplete`](../protocols/services/types/services.incomplete.md), then `eos` | Some initial work timed out, lost its provider, or failed at a swarm member. Keep current offerings; the named services may lack results. |
| `error_message`, then close before any update | Invalid arguments, or `follow` without `services`; no provider was evaluated. |
| apphost `error_msg{denied}` | Session admission failed; a token-less session cannot discover under the default gate. |
| Close before `eos` | Discovery failed; this is not a successful empty result. |

`Available: false` is a provider's answer. A filtered offering is never sent,
so it reads as an absent provider. `services.incomplete` is partial completion,
not discovery failure; it names services, never providers or nodes. A follow can receive later updates
after an incomplete initial attempt.

### Who sees an offering

Every caller may discover; the requesting node filters what reaches it. An
offering of provider `P` for service `S` on node `N` reaches the caller when
`P` is open on `N` and the caller is a swarm caller, or when the caller holds
[`mod.services.service_discovery_action`](../protocols/services/types/mod.services.service_discovery_action.md)
for `S` on `N`.

* **Swarm caller:** an app hosted on a node of the user's swarm, the user, or a
  node of the swarm. A friend's app or node is not a swarm caller.
* **Open:** the binding advertised `open: true`, the default, and no entry of
  `N`'s private list covers it.

| Caller | Open `player` | Private `bitcoin-wallet` |
|--------|---------------|--------------------------|
| Swarm app without permits | shown | hidden |
| Swarm app with a permit for `bitcoin-wallet` | shown | shown |
| Friend's app without permits | hidden | hidden |
| The user | shown | shown |

Every provider of a discovered service is asked, so a private provider learns
who asked even when the answer is filtered. Asks always carry the caller
identity. A consumer that must reach one specific provider pins its
`ProviderID`.

The user holds the action for all services; swarm members hold it on other
members. The node has no default grant for its own identity.

The user can hide a provider without changing the app: an entry of the node's
[`mod.services.private_list`](../protocols/services/types/mod.services.private_list.md)
at `/mod/services/private` makes the providers it covers private. An entry
never makes a private provider open; a permit shows a private provider to the
app that holds it.

```shellsession
$ echo '{"Type":"mod.services.private_list","Object":{"Entries":[{"Service":"player","ProviderID":null}]}}' \
    | astral-query tree.set -path /mod/services/private -in json
```

An app needs a scoped grant or contract to see private providers. A
[`mod.services.discovery_scope`](../protocols/services/types/mod.services.discovery_scope.md)
pairs services with allowed nodes; an unconstrained permit allows nothing.
An app asks for a scoped grant at registration, in the `GrantPermits` of
[`apphost.register`](../protocols/apphost/ops/apphost.register.md), or later
with [`apphost.request_grant`](../protocols/apphost/ops/apphost.request_grant.md).
The user can grant it on the app's node with
[`apphost.grant`](../protocols/apphost/ops/apphost.grant.md):

```shellsession
$ echo '{"Type":"mod.apphost.grant_request","Object":{"Identity":"<app>","Duration":0,"Permits":[{"Action":"mod.services.service_discovery_action","Constraints":[{"Type":"mod.services.discovery_scope","Object":{"Rules":[{"Services":["player"]}]}}]}]}}' \
    | astral-query apphost.grant -in json
```

Grants for different services add up: an app holding a `player` grant and an
`inference` grant sees the private providers of both services.

A rule with no `Nodes` allows its services on every node within discovery's reach.

## Discovering across the swarm

`reach=local` uses hosted providers. `reach=swarm` also queries every other
[Local Swarm](../core-definitions/local-swarm.md) member and merges the results:

```text
App -- discover(reach=swarm) --> Hosting node
                                  |-- evaluate local providers for App
                                  +-- discover(for=App, reach=local) --> Member
                                                                         |
                                             evaluate member's providers for App
```

The hosting node pushes the app's relay contract before querying a member as
itself with `for=App`. The member checks the sending node's
[`relay_for_action`](../protocols/nodes/types/mod.nodes.relay_for_action.md) and
discovery permission, then evaluates all its providers for the app and tags each
offering with the provider's visibility on the member. The hosting node filters
the tagged offerings by the app's permits. Forwarding stops there. The
[discovery reference](../protocols/services/ops/services.discover.md) defines member failure, incomplete results, and follow retries.

## Using an offering

The consumer addresses an offered operation to `ProviderID`, for example
`<ProviderID>:player.play`. Local providers are reached directly; remote apps
are reached through their hosting node under a relay contract. Native node
services are addressed to the node identity. [App Routing](app-routing.md)
defines these routes. Each operation checks permission when invoked.

## Lifetimes and limits

The [advertise reference](../protocols/services/ops/services.advertise.md) limits
one binding to 1–64 distinct names: each name is non-empty, contains no comma
or surrounding whitespace, and fits `string8`. Only one live binding owns each
`(provider, name)` pair; a reconnect can conflict until the old binding closes.

A node restart ends all bindings and discovery streams. Providers advertise
again; consumers discover again. astrald's initial budget is 5 s, request timeout
10 s, and consumer write timeout 10 s. These values are implementation settings,
not protocol constants.
