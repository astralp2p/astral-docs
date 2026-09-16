# mod.objects.repository_info

Summary information about a registered repository.

## Fields

* Name (string8) – Repository name as registered with the module (e.g. `local`, `mem0`).
* Label (string8) – Human-readable label describing the repository.
* Free (uint64) – Free bytes available in the repository. For a group, `Free` is the sum of the free bytes its members report. A member that reports unknown free space adds nothing to the sum. A member that fails to report makes the group's `Free` `0`. The field is unsigned; a negative value is not representable.

## Example

```json
{
  "Type": "mod.objects.repository_info",
  "Object": {
    "Name": "local",
    "Label": "Local storage",
    "Free": 549755813888
  }
}
```
