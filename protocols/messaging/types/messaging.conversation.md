# messaging.conversation

One correspondent of a mailbox. Carried by
[`messaging.conversation_page`](messaging.conversation_page.md) and
[`messaging.conversation_changes`](messaging.conversation_changes.md).

**A conversation whose rows are all archived has no latest message.** It is a
tombstone: pages leave it out, and change reads answer it, so a follower drops
the conversation. A later arrival, or an archived row taken back out, gives it a
latest message again.

## Fields

* Peer ([identity](../../../primitive-types/identity.md)) – The other party: the
  sender of the conversation's inbox rows and the recipient of its outbox rows.
  The mailbox's own identity for a note it wrote to itself.
* Latest (optional [messaging.envelope](messaging.envelope.md)) – The
  unarchived row with the greatest `Cursor`, without its body. Absent for a
  tombstone.
* Unread (uint64) – How many inbox rows from the peer are neither read nor
  archived.
* Rev (uint64) – The conversation's position in the node's order of changes. A
  conversation takes a new, greater one when its latest row, that row's
  envelope, or its unread count changes.

## Example

```json
{
  "Type": "messaging.conversation",
  "Object": {
    "Peer": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "Latest": null,
    "Unread": 0,
    "Rev": 926
  }
}
```
