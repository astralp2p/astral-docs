# mod.services.discovery_rule

One rule in a [`mod.services.discovery_scope`](mod.services.discovery_scope.md),
pairing allowed services with contributing nodes. Empty `Services` allows
nothing; empty `Nodes` allows those services on any node within discovery's reach.

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
