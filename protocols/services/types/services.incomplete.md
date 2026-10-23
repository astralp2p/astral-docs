# services.incomplete

The incomplete outcome of the initial attempt of a
[`services.discover`](../ops/services.discover.md) stream. It is sent at most
once, immediately before the `eos` that ends the initial attempt, and only when
some initial evaluation did not resolve before the node's budget expired or its
provider was lost, or, with `reach=swarm`, when a swarm member could not be
reached, refused, did not finish in time, or reported its own
`services.incomplete`.

A `services.incomplete` is not a failure of the discovery. Every offering the
stream delivered before it is valid; only the named services may lack
offerings. With `follow`, an answer that arrives after the budget still reaches
the stream as a [`services.update`](services.update.md). See
[Services § Reading the outcome](../../../topics/services.md#reading-the-outcome).

A bare `eos` with no preceding `services.incomplete` means the initial attempt
completed: every provider and swarm member the attempt asked answered,
including those that offered nothing.

`Services` names requested services whose initial work did not resolve. It never
names a provider or a node.

## Fields

* Services (array of string8) – Requested services with unresolved initial work.

## Example

```json
{
  "Type": "services.incomplete",
  "Object": { "Services": ["player"] }
}
```
