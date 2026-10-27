# services.incomplete

An unresolved initial outcome on a
[`services.discover`](../ops/services.discover.md) stream. It appears at most
once, immediately before `eos`, when:

* initial evaluation times out or loses its provider;
* a swarm member is unreachable, refuses, times out, or reports incomplete work.

`Services` lists affected requested services, never providers or nodes.
Received offerings remain valid; this is not discovery failure. With `follow`,
later answers can still arrive as [`services.update`](services.update.md).
A bare `eos` means all initial work completed, including unavailable answers.
See [consumer outcomes](../../../topics/services.md#reading-the-outcome).

## Fields

* Services (array of string8) – Requested services with unresolved initial work.

## Example

```json
{
  "Type": "services.incomplete",
  "Object": { "Services": ["player"] }
}
```
