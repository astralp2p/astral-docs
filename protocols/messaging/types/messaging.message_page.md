# messaging.message_page

One page of a mailbox, newest first. Returned by
[`messaging.page_messages`](../ops/messaging.page_messages.md).

## Fields

* Messages ([]messaging.listed_message) – At most the request's `limit` rows, in
  descending `Cursor` order. Empty when nothing is left.
* NextBefore (uint64) – The `before` of the next older page: the `Cursor` of the
  last row answered. 0 when no older row exists.
* Rev (uint64) – The newest revision the node had given when it read the page.
  A caller following the mailbox's changes passes the first page's `Rev` as
  `since` and misses nothing written after the page was read.
* Generation (uint64) – The mailbox's generation. A caller passes it back with
  every position this page gave.

## Example

```json
{
  "Type": "messaging.message_page",
  "Object": {
    "Messages": [],
    "NextBefore": 0,
    "Rev": 921,
    "Generation": 0
  }
}
```
