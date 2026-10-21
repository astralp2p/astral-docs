# mod.nearby.status_message

The status payload broadcast by a node to nearby peers, carrying a bundle of attached objects assembled by registered composers.

## Fields

* Attachments (bundle) – Bundle of objects representing the node's current status.

## Example

```json
{
  "Type": "mod.nearby.status_message",
  "Object": {
    "Attachments": [
      {
        "Type": "mod.dir.alias",
        "Object": "alice"
      }
    ]
  }
}
```
