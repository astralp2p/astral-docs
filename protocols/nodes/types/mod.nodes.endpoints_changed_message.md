# mod.nodes.endpoints_changed_message

A message a node pushes to its linked [Local Swarm](../../../core-definitions/local-swarm.md)
members after its own set of advertised endpoints changed. It asks the receiver to pull the
endpoints of `Subject` from the sender with
[`nodes.resolve_endpoints`](../ops/nodes.resolve_endpoints.md). It carries no endpoints.

A receiver that got the message from `Subject` itself forwards it once to its own linked
local swarm members. A forwarded message is never forwarded again.
[Endpoint exchange in the local swarm](../README.md#endpoint-exchange-in-the-local-swarm)
describes the checks and the effects.

## Fields

* Subject (identity) – The node whose endpoints changed.

## Example

```json
{
  "Type": "mod.nodes.endpoints_changed_message",
  "Object": {
    "Subject": "035d6bfc7818844824354bd5ba1b7c08510139de14aa574e3f53a490814e3eab0e"
  }
}
```
