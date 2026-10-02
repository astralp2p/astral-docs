# services

The `services` protocol lets an app ask its hosting node what providers offer
to that app, and follow changes to those offerings.

An offering is caller-specific. A provider evaluates each caller on its own and
returns a complete [`services.update`](types/services.update.md) for that caller:
two apps asking the same provider for the same service can receive different
operations and terms, or nothing at all. An offering is keyed by a
[`services.offering_key`](types/services.offering_key.md): the provider identity
and the service name.

A service `Name` is free text chosen by whoever defines the service contract,
such as `player`, `bitcoin-wallet` or `contacts-backend`. It need not equal an
operation namespace. A name never contains a comma.

Two operations are exposed:

* [`services.advertise`](ops/services.advertise.md) opens a binding between a
  provider app and its node for a fixed set of service names. While the binding
  is open the node sends [`services.ask`](types/services.ask.md) to evaluate a
  caller and the provider replies with [`services.answer`](types/services.answer.md);
  the provider sends [`services.change`](types/services.change.md) when some
  callers' offerings may have changed.
* [`services.discover`](ops/services.discover.md) evaluates the requested
  services for the caller and streams the offerings, once or following later
  changes.

The node itself offers services too, such as `nat` and `gateway`. Their
`ProviderID` is the node identity.

Discovery starts at the app's own node. By default the node answers from
providers it hosts; with `reach=swarm` it also carries the discovery to every
member of its local swarm in the app's name, and each member answers from the
providers it hosts. `services.advertise` is rejected when it arrives over a
[`Link`](../../core-definitions/link.md). `services.discover` accepts a query
over a `Link`; the caller is the identity that sent the query, or the app it
names in `for`.
Discovering a service requires
[`mod.services.service_discovery_action`](types/mod.services.service_discovery_action.md)
for that service. Discovering an offering grants nothing beyond it: every
operation an offering lists checks its own permission when it runs.

Services state lives only as long as the node process: a node restart ends every
binding and every discovery stream, and providers and consumers open new ones.

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
