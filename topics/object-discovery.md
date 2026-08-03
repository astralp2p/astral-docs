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
  reaches. `objects.search` consults searchers on other `Nodes` only when the `Zone` includes
  `network`.

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
* It answers where the bytes might be fetched from, not whether a fetch will succeed. A provider
  named by a `Finder` may be unreachable, may no longer hold the `Object`, or may refuse to serve
  it.
