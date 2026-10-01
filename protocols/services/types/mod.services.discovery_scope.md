# mod.services.discovery_scope

The constraint that narrows a permit for
[`mod.services.service_discovery_action`](mod.services.service_discovery_action.md)
to pairs of service and contributing node.

The scope allows a pair when one of its rules allows it. Rules keep their
service and node lists paired: a scope with a rule for `player` on any node and
a rule for `bitcoin-wallet` on one node does not allow `bitcoin-wallet` on any
other node.

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
