# messaging.conversation_changes

The conversations of a mailbox that changed after a revision, oldest change
first. Returned by
[`messaging.list_conversation_changes`](../ops/messaging.list_conversation_changes.md).

## Fields

* Conversations ([]messaging.conversation) – At most the request's `limit`
  conversations, in ascending `Rev` order, each at its latest state, tombstones
  included.
* NextRev (uint64) – The `since` of the next read: the `Rev` of the last
  conversation answered, or the request's `since` when none is answered.
* More (bool) – Conversations remain after `NextRev`.
* Generation (uint64) – The mailbox's generation.

## Example

```json
{
  "Type": "messaging.conversation_changes",
  "Object": {
    "Conversations": [],
    "NextRev": 921,
    "More": false,
    "Generation": 0
  }
}
```
