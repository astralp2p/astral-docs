# mod.objects.repository_info

Summary information about a registered repository.

## Fields

* Name (string8) – Repository name as registered with the module (e.g. `local`, `mem0`).
* Label (string8) – Human-readable label describing the repository.
* Free (uint64) – Free bytes available in the repository. For a group, `Free` is the sum of the free bytes its members report. A member that reports unknown free space adds nothing to the sum. A member that fails to report makes the group's `Free` `0`. The field is unsigned; a negative value is not representable.
* Kind (string8) – `repository` for a repository that stores objects itself, or `group` for a repository group that delegates to its members.
* Children ([]string8) – Names of the direct members of a group, in lookup order. Each name references another registered repository. `Children` is `[]` for a `repository` and for a group with no members.
* Concurrent (bool) – For a group, `true` races a read across all members and returns the first successful result, and `false` tries members in `Children` order. `Concurrent` governs reads only. `Concurrent` is `false` for a `repository`.

## Group lookup

A group stores no object, so it answers
[`objects.read`](../ops/objects.read.md),
[`objects.contains`](../ops/objects.contains.md) and
[`objects.delete`](../ops/objects.delete.md) from its members. A `repository`
answers for itself, and none of the rules below apply to it.

* A group passes the [`Object ID`](../../../core-definitions/object-id.md) to a
  member unchanged, whether or not its `Size` is 0, and answers a successful
  member unchanged.
* A name in `Children` that references no registered repository is skipped. A
  skipped name is not an invoked member.
* A group no member answers successfully returns `false` for
  `objects.contains`, and the not-found `error_message` for `objects.read` and
  `objects.delete`. A group with no invoked member returns the same.
* A member failure other than an unsupported `Hash` lookup — an excluded
  [`Zone`](../../../core-definitions/zone.md), a read error, two stored objects
  sharing the `Hash` of a `Partial Object ID` — leaves that member contributing
  nothing, and the group answers as though the member found no object. A
  member's failure is never relayed as the group's own.
* A group reports an unsupported `Hash` lookup only when it invokes at least
  one member and every invoked member reports one. Its `error_message` then
  carries the text `hash lookup: unsupported operation`. One invoked member
  that looks up by `Hash` and finds no object makes the whole group find no
  object.
* A group holding groups applies these rules at each level: an inner group's
  answer is one member's answer to the group above it.
* A group whose call is cancelled reports the cancellation rather than a
  not-found. An `objects.delete` that already succeeded in one member is an
  exception: the group returns `ack`, and the members it did not reach keep
  their copy.

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
