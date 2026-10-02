# messaging.list_conversation_changes

Read every conversation of a mailbox that changed after a revision, oldest
change first. See [Paging](../README.md#paging).

Admission is [`messaging.list_messages`](messaging.list_messages.md)'s: the
caller's own mailbox, or the one `mailbox` names as a
[delegated read](../README.md#delegated-read), checked in the same order and
refused the same way. A refused caller receives no bytes. Local-only — queries
from the network are rejected, and so are queries carrying the `mcp` origin.
The operation stamps nothing read and tells no sender anything.

Conversations are answered in ascending `Rev` order, each at its latest state.
A conversation whose last unarchived message was put away is answered with no
`Latest`: a follower drops it. The operation answers at most `limit`
conversations and reads one past the limit to set `More`.

The answer is one object followed by an `eos` object, or one `error_message`
object. A caller applies nothing it read before the `eos`: an object without
its `eos` is no answer.

## Arguments

* since (uint64) – Reads only conversations whose `Rev` is above this one: the
  `Rev` of the first page a caller read, or the `NextRev` of an earlier answer.
  Defaults to 0.
* limit (uint64) – The most conversations answered. 0 reads 50. A value over
  100 is refused.
* generation (uint64) – The `Generation` of the answer that gave `since`.
  Required. A value that is not the mailbox's generation is refused.
* mailbox (string8) – As [`messaging.list_messages`](messaging.list_messages.md)
  takes it.

## Returned objects

Once the query is accepted, the operation checks again that this node hosts the
mailbox, then checks `since` and `limit`, reads the conversations, and checks
`generation`, in that order. The first failure is the answer.

The operation returns one of:
* An `error_message` object reading `not a messaging participant` if this node
  stopped hosting the mailbox after the query was accepted.
* An `error_message` object reading
  `since is a position a previous answer gave you, not <since>` if `since` is
  over 9223372036854775807.
* An `error_message` object reading `limit is at most 100, not <limit>` if
  `limit` is over 100.
* An `error_message` object reading `generation is required with a position` if
  `generation` is absent.
* An `error_message` object reading
  `generation changed: the mailbox was deleted since this position was read` if
  `generation` is not the mailbox's.
* An `error_message` object if the rows cannot be read.
* A
  [`messaging.conversation_changes`](../types/messaging.conversation_changes.md)
  object, followed by an `eos` object.

## Examples

```shellsession
$ astral-query messaging.list_conversation_changes -since 921 -generation 0 -out json
{"Type":"messaging.conversation_changes","Object":{"Conversations":[{"Peer":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Latest":null,"Unread":0,"Rev":926}],"NextRev":926,"More":false,"Generation":0}}
{"Type":"eos","Object":null}
```
