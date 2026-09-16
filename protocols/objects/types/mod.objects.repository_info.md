# mod.objects.repository_info

Summary information about a registered repository.

## Fields

* Name (string8) – Repository name as registered with the module (e.g. `local`, `mem0`).
* Label (string8) – Human-readable label describing the repository.
* Free (uint64) – Free bytes available in the repository. For a group, `Free` is the sum of the free bytes its members report. A member that reports unknown free space adds nothing to the sum. A member that fails to report makes the group's `Free` `0`. The field is unsigned; a negative value is not representable.
* Kind (string8) – `repository` for a repository that stores objects itself, or `group` for a repository group that delegates to its members.
* Children ([]string8) – Names of the direct members of a group, in lookup order. Each name references another registered repository. `Children` is `[]` for a `repository` and for a group with no members.
* Concurrent (bool) – For a group, `true` races a read across all members and returns the first successful result, and `false` tries members in `Children` order. `Concurrent` governs reads only. `Concurrent` is `false` for a `repository`.

## Example

```json
{
  "Type": "mod.objects.repository_info",
  "Object": {
    "Name": "memory",
    "Label": "In-memory repos",
    "Free": 134217657,
    "Kind": "group",
    "Children": [
      "mem0",
      "system"
    ],
    "Concurrent": false
  }
}
```
