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

[`services.discover`](../protocols/services/ops/services.discover.md) requests named
services from the app's node; there is no discover-all operation. Admission fixes
the initial contributions: local providers for the requested services, plus swarm
members when `reach=swarm`. The node evaluates them for the caller and streams
available offerings as they arrive.

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
| `services.update`, `Available: true` | Add or replace the offering for `(ProviderID, Name)`. |
| `services.update`, `Available: false` | The provider withdraws a previously shown offering; remove that key. An initially unavailable offering is not sent. |
| [`services.removed`](../protocols/services/types/services.removed.md) | A provider or contributing swarm member was lost; remove the listed keys. |
| `eos` without `services.incomplete` | Initial evaluation completed, including unavailable answers. No offerings can mean no providers or no available answers. |
| [`services.incomplete`](../protocols/services/types/services.incomplete.md), then `eos` | Some initial work timed out, lost its provider, or failed at a swarm member. Keep current offerings; the named services may lack results. |
| `error_message`, then close before any update | Invalid arguments or missing discovery permission; no provider was evaluated. |
| apphost `error_msg{denied}` | Session admission failed; a token-less session cannot discover under the default allowlist. |
| Close before `eos` | Discovery failed; this is not a successful empty result. |

`Available: false` is a provider's answer. Permission refusal prevents asking
providers. `services.incomplete` is partial completion, not discovery failure;
it names services, never providers or nodes. A follow can receive later updates
after an incomplete initial attempt.

### Who may discover

Admission requires
[`mod.services.service_discovery_action`](../protocols/services/types/mod.services.service_discovery_action.md)
for every requested service on every contributing node. One denied pair refuses
the whole request. The user holds the action for all services; swarm members
hold it on other members. The node has no default grant for its own identity.

An app needs a scoped grant or contract. A
[`mod.services.discovery_scope`](../protocols/services/types/mod.services.discovery_scope.md)
pairs services with allowed nodes; an unconstrained permit allows nothing.
An app cannot grant itself discovery at registration. The user can grant it on
the app's node:

```shellsession
$ echo '{"Type":"bundle","Object":[{"Type":"mod.services.discovery_scope","Object":{"Rules":[{"Services":["player"]}]}}]}' \
    | astral-query apphost.grant -identity <app> -action mod.services.service_discovery_action -constrained true -in json
```

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

The hosting node checks the app's scope across all contributing nodes. It pushes
the app's relay contract before querying a member as itself with `for=App`.
The member checks the sending node's
[`relay_for_action`](../protocols/nodes/types/mod.nodes.relay_for_action.md) and
discovery permission, then evaluates providers for the app. Forwarding stops
there. The [discovery reference](../protocols/services/ops/services.discover.md)
defines member failure, incomplete results, and follow retries.

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
