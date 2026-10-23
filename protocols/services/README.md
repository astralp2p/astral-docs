# services

The `services` protocol discovers caller-specific offerings and follows changes.
Each [`services.update`](types/services.update.md) is a complete offering keyed
by [(provider identity, service name)](types/services.offering_key.md). A service
name identifies a contract, such as `player`; it need not match an operation
namespace. An offering grants no permission to invoke its operations.

| Operation | Purpose |
|-----------|---------|
| [`services.advertise`](ops/services.advertise.md) | Bind a local provider app to a fixed set of service names. |
| [`services.discover`](ops/services.discover.md) | Evaluate named services for the caller, once or with `follow`. |

```text
Provider                       Node                        Consumer
   |-- advertise ------------->|                               |
   |<-- ack -------------------|<-- discover -------------------|
   |<-- ask(caller, service) ---|                               |
   |-- answer(update) -------->|-- update, if available ------->|
   |                           |-- [incomplete], eos ---------->|
   |-- change(callers) -------->| re-evaluate for followers      |
```

Discovery defaults to hosted providers. `reach=swarm` also queries local swarm
members for the app; each member evaluates only its hosted providers. Native
node services use the node identity as `ProviderID`. A node restart ends all
bindings and streams; providers and consumers reopen them.

## Protocol rules

* Advertising requires the caller's app identity and
  [`mod.auth.serve_apps_action`](../auth/types/mod.auth.serve_apps_action.md).
  [`apphost.register`](../apphost/ops/apphost.register.md) requests the grant.
  The node identity and queries arriving over a link are rejected. See
  [Session Identity](../../topics/session-identity.md).
* An [answer](types/services.answer.md) echoes the ask's `RequestID`.
  `Update.Name` must equal the asked `Service`; a mismatch fails the binding
  and removes its shown offerings.
* `Available: false` is a provider's answer. A refused discovery returns
  `error_message` before evaluating providers. Admission requires
  [`service_discovery_action`](types/mod.services.service_discovery_action.md)
  for every requested service on every contributing node.
* [`services.incomplete`](types/services.incomplete.md) precedes `eos` when
  initial work remains unresolved or fails. It does not invalidate received
  offerings. A close before `eos` is discovery failure.

The [Services topic](../../topics/services.md) provides examples and the
[consumer outcome table](../../topics/services.md#reading-the-outcome).

## Types

* [`services.update`](types/services.update.md) – one complete offering
* [`services.offering_key`](types/services.offering_key.md) – provider identity and service name
* [`services.operations_list`](types/services.operations_list.md) – operations an offering exposes
* [`services.ask`](types/services.ask.md) – node to provider: evaluate one service for one caller
* [`services.answer`](types/services.answer.md) – provider to node: the evaluated offering
* [`services.change`](types/services.change.md) – provider to node: some callers' offerings may have changed
* [`services.incomplete`](types/services.incomplete.md) – the initial attempt did not complete
* [`services.removed`](types/services.removed.md) – shown offerings whose provider was lost
* [`mod.services.service_discovery_action`](types/mod.services.service_discovery_action.md) – discover one service on one node
* [`mod.services.discovery_scope`](types/mod.services.discovery_scope.md) – the services and nodes a discovery permit allows
* [`mod.services.discovery_rule`](types/mod.services.discovery_rule.md) – one rule of a discovery scope
