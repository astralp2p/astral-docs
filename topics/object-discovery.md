# Object Discovery

* A [`Node`](../core-definitions/node.md) stores an [`Object`](../core-definitions/object.md) under its
  [`Object ID`](../core-definitions/object-id.md), a hash of the object's canonical bytes. The
  `Object ID` says nothing about what the `Object` means, who holds it, or how to find it again.
* `Object Discovery` is the set of [`Ops`](../core-definitions/op.md) that answer those questions
  without reading the `Object`: `objects.search` — which objects match a description;
  `objects.describe` — what is known about this object; `objects.find` — who can provide its bytes.
* A `Node` answers none of them from its own knowledge. Each `Op` is a fan-out across a registry of
  providers, and the answer is whatever those providers return, merged into one stream. The `Node`
  holds the registry, not the index.

## Roles

| Role        | Question                       | Op                 | Result stream                |
|-------------|--------------------------------|--------------------|------------------------------|
| `Searcher`  | which objects match this query | `objects.search`   | `mod.objects.search_result`  |
| `Describer` | what is known about this object| `objects.describe` | `mod.objects.describe_result`|
| `Finder`    | who can provide this object    | `objects.find`     | [`identity`](../primitive-types/identity.md)                   |

* Each role is a separate registry. A provider is either a module compiled into the `Node` or an
  [`App`](../core-definitions/app.md) registered at runtime — see
  [External Providers](external-providers.md). The two are indistinguishable to a caller.
* A provider never sees the other providers and is never asked to agree with them. It answers what
  it knows, or it answers nothing.

## Fan-out

* A discovery `Op` calls every registered provider of its role concurrently and merges their streams
  into one. Result order across providers is not defined.
* A provider that fails or refuses contributes nothing to that call; the `Op` still succeeds with
  whatever the others returned. An empty stream is a valid answer, not an error.
* The stream ends with an [`eos`](../primitive-types/eos.md) once every provider has finished. Each
  discovery `Op` bounds its fan-out with a timeout; results already sent stand.
* Every result carries a `SourceID` — the [`Identity`](../core-definitions/identity.md) of the
  provider that produced it. Discovery answers are attributed, never anonymous, so a caller can
  weigh or ignore a source rather than trusting a merged verdict.
* A [`Zone`](../core-definitions/zone.md) accompanies the call and bounds how far the fan-out
  reaches. The `zone` argument of `objects.read`, `objects.find`, `objects.search` and
  `objects.describe` limits the query's routing zone and never widens it. `device` permits device
  providers, `virtual` permits virtual providers, and `network` permits other `Nodes`. `dv` keeps
  the call on this `Node`; `dvn` also reaches its swarm.
* The `Zone` filters the scope; it grants no access. Authorization is
  [`mod.auth.see_objects_action`](../protocols/auth/types/mod.auth.see_objects_action.md), decided
  before the fan-out.

## Swarm

* With `network`, a `Node` reaches the other members of its swarm in two ways:
  * Swarm providers are registered providers like any other. The swarm `Finder` asks every member
    [`objects.contains`](../protocols/objects/ops/objects.contains.md); the swarm `Searcher` and
    swarm `Describer` forward the call to every member.
  * `sources` names `Nodes` the caller chooses, on `objects.search` and `objects.describe`.
    `sources_only` asks them alone, without the registered providers; without it they are asked on
    top of the providers.
* The `Node` authorizes its caller, then asks other `Nodes` as itself. A swarm member holds
  `mod.auth.see_objects_action` and trusts that authorization.
* A query arriving from another `Node` runs without the `network` zone, so the receiving `Node`
  answers from its own providers and never asks back.

## Searching

* `objects.search` parses its `q` argument into an
  [`objects.search_query`](../protocols/objects/types/objects.search_query.md): bare words become the
  free-text portion, `tag:value` tokens become
  [`objects.query_tag`](../protocols/objects/types/objects.query_tag.md) clauses. Names and values are
  lowercased on parse; double quotes carry values containing spaces.
* A tag carries one of four modifiers: `tag:value` requires, `-tag:value` excludes, `?tag:value`
  optionally includes, `~tag:value` optionally excludes.
* Required and excluded tags bind: a `Searcher` that does not understand one refuses the query
  rather than answering it partially. Optional tags are hints a `Searcher` may ignore. The
  distinction is what lets a single query address searchers with different vocabularies — the query
  states what it must have and what it would merely like, and each `Searcher` decides whether it can
  honour the must.
* An empty query matches everything.
* Matches are deduplicated by `Object ID` across all providers, so two searchers finding the same
  `Object` yield one [`mod.objects.search_result`](../protocols/objects/types/mod.objects.search_result.md).
  The `repo` argument narrows the stream to objects a named repository contains.

## Describing

* `objects.describe` streams one
  [`mod.objects.describe_result`](../protocols/objects/types/mod.objects.describe_result.md) per
  descriptor. A descriptor's `Data` is an `Object` of any type, not text: meaning travels as an
  [`Object Type`](../core-definitions/object-type.md), so a consumer selects what it understands by
  type instead of parsing prose.
* An `Object` has no single description. Every `Describer` contributes what it knows — one describes
  the bytes, another the media they decode to, a third where the object was seen — and the caller
  receives all of them side by side. Nothing reconciles them; descriptors that disagree are a normal
  result, and choosing between them is the caller's decision.
* A `Describer` with nothing to say about an `Object ID` returns an empty stream. Not-found is
  silence, not an error.
* The `only` and `except` arguments filter the stream by descriptor type.

## Finding

* `objects.find` streams the `Identities` believed to be able to provide the `Object`, deduplicated
  by their string form.
* Two `Finders` are built in. The local `Finder` names this `Node` when its read-default repository
  holds the `Object`. The swarm `Finder` names each swarm member that answers `objects.contains`
  true, and runs only with `network`.
* It answers where the bytes might be fetched from, not whether a fetch will succeed. A provider
  named by a `Finder` may be unreachable, may no longer hold the `Object`, or may refuse to serve
  it.

## Reading

* [`objects.read`](../protocols/objects/ops/objects.read.md) without `repo` uses finding to locate
  bytes. Each identity the finders name is a candidate; candidates are tried concurrently as they
  arrive, and the first to deliver supplies the read.
* A failed attempt before bytes reach the caller gives way to the other candidates. A failure after
  fails the read.
* A search result, a descriptor, or a found identity grants no read access. Reading remains a
  separate, authorized step.
