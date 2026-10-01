# services.incomplete

The incomplete outcome of the initial attempt of a
[`services.discover`](../ops/services.discover.md) stream. It is sent at most
once, immediately before the `eos` that ends the initial attempt, and only when
some initial evaluation did not resolve before the node's budget expired or its
provider was lost.

A bare `eos` with no preceding `services.incomplete` means the initial attempt
completed: every provider the attempt asked answered, including providers that
offered nothing.

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
