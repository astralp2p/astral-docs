# mod.services.discovery_rule

One rule of a [`mod.services.discovery_scope`](mod.services.discovery_scope.md):
the services a holder may discover, on the nodes it may discover them on.

A rule with an empty `Services` list allows nothing. A rule with an empty
`Nodes` list allows its services on any node within the discovery's reach.

## Fields

* Services (array of string8) – Service names the rule allows.
* Nodes (array of identity) – Contributing nodes the rule allows; empty allows any node within reach.

## Example

```json
{
  "Type": "mod.services.discovery_rule",
  "Object": {
    "Services": ["player"],
    "Nodes": []
  }
}
```
