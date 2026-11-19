# mod.nodes.endpoints_updated_event

Emitted by nodes when a pull that a
[`mod.nodes.endpoints_changed_message`](mod.nodes.endpoints_changed_message.md) started
stored at least one new endpoint of `Identity`. It travels as the `Data` of a
[`mod.events.event`](../../events/types/mod.events.event.md) to the node's own receivers and
never leaves the node.

A new endpoint is one the node held no unexpired row for, by network and address, before
the pull. The user module wakes the link to `Identity` on this event.

## Fields

* Identity (identity) – The node whose endpoints the pull stored.

## Example

```json
{
  "Type": "mod.nodes.endpoints_updated_event",
  "Object": {
    "Identity": "035d6bfc7818844824354bd5ba1b7c08510139de14aa574e3f53a490814e3eab0e"
  }
}
```
