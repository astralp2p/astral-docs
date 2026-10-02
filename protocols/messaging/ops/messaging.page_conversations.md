# messaging.page_conversations

Read one page of a mailbox's conversations, newest first by their latest
message, or the one conversation with a peer. See
[Paging](../README.md#paging).

Admission is [`messaging.list_messages`](messaging.list_messages.md)'s: the
caller's own mailbox, or the one `mailbox` names as a
[delegated read](../README.md#delegated-read), checked in the same order and
refused the same way. A refused caller receives no bytes. Local-only — queries
from the network are rejected, and so are queries carrying the `mcp` origin.
The operation stamps nothing read and tells no sender anything.

A page answers conversations in descending order of their latest message's
`Cursor`, and leaves out every conversation whose rows are all archived. With
`peer`, the operation answers that one conversation whatever its state, or none.
A page holds at most `limit` conversations; the node reads one past the limit
to set `NextBefore`.

The answer is one object followed by an `eos` object, or one `error_message`
object. A caller applies nothing it read before the `eos`: an object without
its `eos` is no answer.

## Arguments

* peer (string8) – Reads the one conversation with this identity, given as a hex
  public key or a name resolved via the directory. Exclusive with `before`.
* before (uint64) – Reads only conversations whose latest message's `Cursor` is
  below this one: the `NextBefore` of an earlier page. Defaults to 0, which
  reads the newest page.
* limit (uint64) – The most conversations answered. 0 reads 50. A value over
  100 is refused.
* generation (uint64) – The `Generation` of the page that gave `before`.
  Required when `before` is nonzero. A value that is not the mailbox's
  generation is refused.
* mailbox (string8) – As [`messaging.list_messages`](messaging.list_messages.md)
  takes it.

## Returned objects

Once the query is accepted, the operation checks again that this node hosts the
mailbox, then checks `peer` with `before`, `before`, `limit` and `peer`'s
resolution, reads the page, and checks `generation`, in that order. The first
failure is the answer.

The operation returns one of:
* An `error_message` object reading `not a messaging participant` if this node
  stopped hosting the mailbox after the query was accepted.
* An `error_message` object reading
  `peer names one conversation; before pages them all` if both are given.
* An `error_message` object reading
  `before is a position a previous answer gave you, not <before>` if `before` is
  over 9223372036854775807.
* An `error_message` object reading `limit is at most 100, not <limit>` if
  `limit` is over 100.
* An `error_message` object reading `unknown correspondent: <name>` if `peer`
  resolves to no identity.
* An `error_message` object reading `generation is required with a position` if
  `before` is nonzero and `generation` is absent.
* An `error_message` object reading
  `generation changed: the mailbox was deleted since this position was read` if
  `generation` is not the mailbox's.
* An `error_message` object if the rows cannot be read.
* A [`messaging.conversation_page`](../types/messaging.conversation_page.md)
  object, followed by an `eos` object.

## Examples

```shellsession
$ astral-query messaging.page_conversations -limit 1 -out json
{"Type":"messaging.conversation_page","Object":{"Conversations":[{"Peer":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Latest":{"Cursor":415,"ID":"0d41e6b28c5a4f9137be0a62d85c7f14","Box":"inbox","Sender":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Recipient":"026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2","ParentID":"7f3a1c9e5b024d6810af2e7c94b5d3a6","CreatedAt":"2026-09-02T22:16:40.215004Z","ArchivedAt":null,"ReadAt":null,"ReceiptDueAt":null,"ReceiptStoredAt":null,"LandedAt":null,"FailedAt":null,"FetchedAt":null,"Err":null},"Unread":1,"Rev":919}],"NextBefore":415,"Rev":921,"Generation":0}}
{"Type":"eos","Object":null}
```
