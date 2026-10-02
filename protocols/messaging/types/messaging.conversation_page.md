# messaging.conversation_page

One page of a mailbox's conversations, newest first by their latest message.
Returned by
[`messaging.page_conversations`](../ops/messaging.page_conversations.md).

## Fields

* Conversations ([]messaging.conversation) – At most the request's `limit`
  conversations, in descending order of their latest row's `Cursor`. A page
  holds no tombstone. A request naming a peer answers that conversation, a
  tombstone included, or none.
* NextBefore (uint64) – The `before` of the next page: the `Cursor` of the last
  conversation's latest row. 0 when no further conversation exists, and always
  0 for a request naming a peer.
* Rev (uint64) – The newest revision the node had given when it read the page.
* Generation (uint64) – The mailbox's generation.

## Example

```json
{
  "Type": "messaging.conversation_page",
  "Object": {
    "Conversations": [],
    "NextBefore": 0,
    "Rev": 921,
    "Generation": 0
  }
}
```
