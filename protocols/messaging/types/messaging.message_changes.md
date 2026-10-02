# messaging.message_changes

The rows of a mailbox that changed after a revision, oldest change first.
Returned by
[`messaging.list_message_changes`](../ops/messaging.list_message_changes.md).

## Fields

* Messages ([]messaging.listed_message) – At most the request's `limit` rows, in
  ascending `Rev` order, each at its latest state. Archived rows are included.
* NextRev (uint64) – The `since` of the next read: the `Rev` of the last row
  answered, or the request's `since` when no row is answered.
* More (bool) – Rows remain after `NextRev`.
* Generation (uint64) – The mailbox's generation.

## Example

```json
{
  "Type": "messaging.message_changes",
  "Object": {
    "Messages": [],
    "NextRev": 921,
    "More": false,
    "Generation": 0
  }
}
```
