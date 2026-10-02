# messaging.page_messages

Read one page of a mailbox, newest first, without the message bodies: one of
the three lists, or every unarchived row exchanged with one peer, in both boxes.
See [Paging](../README.md#paging).

Admission is [`messaging.list_messages`](messaging.list_messages.md)'s: the
caller's own mailbox, or the one `mailbox` names as a
[delegated read](../README.md#delegated-read), checked in the same order and
refused the same way. A refused caller receives no bytes. Local-only — queries
from the network are rejected, and so are queries carrying the `mcp` origin.
The operation stamps nothing read and tells no sender anything.

Rows are answered in descending `Cursor` order. A page holds at most `limit`
rows. The node reads one row past the limit and never answers it: that row
only says whether another page follows. `NextBefore` is the `Cursor` of the
last row answered, so a page that ends exactly at the limit still says whether
another follows.

The answer is one object followed by an `eos` object, or one `error_message`
object. A caller applies nothing it read before the `eos`: an object without
its `eos` is no answer.

## Arguments

* list (string8) – `inbox`, `outbox` or `archive`, as
  [`messaging.list_messages`](messaging.list_messages.md) reads them. Defaults
  to `inbox`. Exclusive with `peer`.
* peer (string8) – Reads the unarchived rows whose other party is this
  identity, from both boxes: the inbox rows it wrote and the outbox rows written
  to it. Given as a hex public key or a name resolved via the directory. A note
  the mailbox's identity writes to itself is answered as both its rows under
  `peer` naming that identity.
* before (uint64) – Reads only rows whose `Cursor` is below this one: the
  `NextBefore` of an earlier page. Defaults to 0, which reads the newest page.
* limit (uint64) – The most rows answered. 0 reads 50. A value over 100 is
  refused.
* generation (uint64) – The `Generation` of the page that gave `before`.
  Required when `before` is nonzero. A value that is not the mailbox's
  generation is refused.
* mailbox (string8) – As [`messaging.list_messages`](messaging.list_messages.md)
  takes it.

## Returned objects

Once the query is accepted, the operation checks again that this node hosts the
mailbox, then checks `list` and `peer`, `before`, `limit` and `peer`'s
resolution, reads the page, and checks `generation`, in that order. The first
failure is the answer.

The operation returns one of:
* An `error_message` object reading `not a messaging participant` if this node
  stopped hosting the mailbox after the query was accepted.
* An `error_message` object reading
  `list and peer are exclusive: peer reads both boxes` if both are given.
* An `error_message` object reading `no such list: <list>` if `list` names none
  of the three.
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
* A [`messaging.message_page`](../types/messaging.message_page.md) object,
  followed by an `eos` object.

## Examples

```shellsession
$ astral-query messaging.page_messages -peer scout -limit 2 -out json
{"Type":"messaging.message_page","Object":{"Messages":[{"Rev":918,"Envelope":{"Cursor":415,"ID":"0d41e6b28c5a4f9137be0a62d85c7f14","Box":"inbox","Sender":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Recipient":"026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2","ParentID":"7f3a1c9e5b024d6810af2e7c94b5d3a6","CreatedAt":"2026-09-02T22:16:40.215004Z","ArchivedAt":null,"ReadAt":null,"ReceiptDueAt":null,"ReceiptStoredAt":null,"LandedAt":null,"FailedAt":null,"FetchedAt":null,"Err":null}},{"Rev":907,"Envelope":{"Cursor":412,"ID":"7f3a1c9e5b024d6810af2e7c94b5d3a6","Box":"outbox","Sender":"026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2","Recipient":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","ParentID":"00000000000000000000000000000000","CreatedAt":"2026-09-02T22:14:07.104829Z","ArchivedAt":null,"ReadAt":null,"ReceiptDueAt":null,"ReceiptStoredAt":null,"LandedAt":"2026-09-02T22:14:07.188203Z","FailedAt":null,"FetchedAt":"2026-09-02T22:15:01.402551Z","Err":null}}],"NextBefore":412,"Rev":921,"Generation":0}}
{"Type":"eos","Object":null}
```

```shellsession
$ astral-query messaging.page_messages -before 412 -out json
{"Type":"error_message","Object":"generation is required with a position"}
```
