# External Providers

* A [`Node`](../core-definitions/node.md) knows how to store, address, and move
  [`Objects`](../core-definitions/object.md). It does not know what any particular `Object` means.
  Meaning enters through [`Apps`](../core-definitions/app.md): an `App` that recognises a kind of
  `Object` registers with its `Node` and becomes part of the answers the `Node` gives to
  [`Object Discovery`](object-discovery.md) calls.
* An `External Provider` is such an `App` — registered at runtime as a `Searcher`, `Describer`, or
  `Finder`. Once registered it is indistinguishable from a provider compiled into the `Node`: the
  same fan-out reaches it, the same result types come back, and callers cannot tell which is which.
* Registration is symmetric rather than a plugin interface. A `Node` answers `objects.describe` by
  calling `objects.describe` on every registered `App`; `objects.search` and `objects.find` work the
  same way. An `External Provider` serves the very [`Op`](../core-definitions/op.md) it extends, with
  the same arguments, the same result types, and the same stream terminated by
  [`eos`](../primitive-types/eos.md). For that one `Op`, an `App` is shaped like a `Node`.
* This is what keeps the `objects` protocol closed while the knowledge behind it stays open: no new
  op, no new type, and no privileged extension point is needed to teach a `Node` about a new kind of
  `Object`.

## Registering

* Three `Ops` register the caller: `objects.register_searcher`, `objects.register_describer`,
  `objects.register_finder`. None takes arguments beyond `in` and `out` — the `Node` takes the
  registrant from the caller's [`Identity`](../core-definitions/identity.md), so an `App` cannot
  register anybody but itself.
* Registration is node-local. A [`Query`](../core-definitions/query.md) arriving over the network is
  rejected: an `App` may extend the `Node` hosting it, never a remote one. The `Node` also refuses a
  missing or zero caller `Identity`, and refuses to register itself.
* Registration is keyed by the caller's `Identity`, one per `Identity` per role. Repeating it is a
  no-op, so an `App` may register whenever it is unsure whether it already has.
* The `Node` answers with an [`ack`](../primitive-types/ack.md) and routes the matching discovery
  call to that `Identity` for the lifetime of the registration. A `Node` does not keep a registration
  on an `App`'s behalf across its own restart; an `App` re-registers when it reconnects.
* Every result an `External Provider` returns is stamped by the `Node` with the registered
  `Identity` as its `SourceID`, replacing whatever the `App` set. A provider cannot attribute its
  answers to another `Identity`.
* Each proxied call runs under its own timeout, so a provider that stops answering delays only its
  own contribution to the fan-out.

## Serving search

* A registered `Searcher` serves `objects.search`: it parses `q` as an
  [`objects.search_query`](../protocols/objects/types/objects.search_query.md), streams one
  [`mod.objects.search_result`](../protocols/objects/types/mod.objects.search_result.md) per match,
  and ends with `eos`.
* A `Searcher` declares the tag names it understands. A query carrying a required (`tag:value`) or
  excluded (`-tag:value`) tag outside that vocabulary is refused rather than answered: the caller
  asked for a constraint the `Searcher` cannot apply, and answering anyway would present matches as
  satisfying a filter that was never applied. Optional tags (`?tag:value`, `~tag:value`) outside the
  vocabulary are ignored — that is what makes them optional.
* Refusing is cheap and local. The fan-out drops the refusing provider and the other searchers still
  answer, so a query may name tags only some searchers know.
* Matches are deduplicated by [`Object ID`](../core-definitions/object-id.md) on the `Node`, so an `App` that fans out internally need
  not deduplicate its own stream.

## Serving describe

* A registered `Describer` serves `objects.describe`: it streams one
  [`mod.objects.describe_result`](../protocols/objects/types/mod.objects.describe_result.md) per
  descriptor and ends with `eos`.
* The descriptor's `Data` carries the meaning — a typed `Object` the `App` produces from its own
  index. A descriptor with no `Data` carries nothing and is dropped.
* An `Object ID` the `App` does not recognise yields an empty stream. A `Describer` describes what it
  knows and stays silent about the rest; silence is not a failure and does not affect the other
  describers' contributions.

## Publishing types

* A descriptor's `Data` is usually a type the `App` defines rather than a primitive.
  `App`-defined [`Object Types`](../core-definitions/object-type.md) are conventionally named
  `app.<app>.<type>` — for example `app.media.audio_file` — which keeps an `App`'s vocabulary
  distinct from the `Node`'s built-in types and from every other `App`'s.
* A type is only useful to a receiver that can decode it. An `App` registers a
  [`Blueprint`](blueprints.md) for each of its types through `objects.register_blueprint` before
  serving descriptors that carry them; without one the payload crosses the wire as bytes the
  receiver cannot interpret.
* An `App` reconciles rather than re-registers blindly: `objects.blueprints` lists the type names the
  `Node` already knows, and the `App` registers only what is missing. Blueprints are pushed in
  dependency order, aliases before the structs referencing them, so every reference resolves as it
  is replayed.
* Type registration and provider registration belong to the same connect step. An `App` that
  re-registers after a reconnect republishes its `Blueprints` too, so a `Node` that restarted
  relearns both the vocabulary and who speaks it.
