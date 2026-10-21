# mod.nearby.status

The resolved status of a nearby peer, combining the peer's identity with its attached status objects.

## Fields

* Identity (identity) – The resolved identity of the nearby node.
* Attachments (bundle) – Bundle of objects attached to the node's status.

## Example

```json
{
  "Type": "mod.nearby.status",
  "Object": {
    "Identity": "02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f",
    "Attachments": [
      {
        "Type": "mod.dir.alias",
        "Object": "alice"
      }
    ]
  }
}
```
