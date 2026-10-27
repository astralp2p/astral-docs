# mod.services.discovery_scope

A constraint on
[`mod.services.service_discovery_action`](mod.services.service_discovery_action.md).
A `(service, node)` pair is allowed when one rule matches both values; lists
from different rules are never combined.

The example allows `player` on any node within reach and `bitcoin-wallet` only
on the named node.

## Fields

* Rules (array of [`mod.services.discovery_rule`](mod.services.discovery_rule.md)) – The rules; empty allows nothing.

## Example

```json
{
  "Type": "mod.services.discovery_scope",
  "Object": {
    "Rules": [
      { "Services": ["player"], "Nodes": [] },
      {
        "Services": ["bitcoin-wallet"],
        "Nodes": ["02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f"]
      }
    ]
  }
}
```
