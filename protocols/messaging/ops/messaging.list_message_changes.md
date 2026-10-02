# messaging.list_message_changes

Read every row of a mailbox written or changed after a revision, oldest change
first, without the message bodies. See [Paging](../README.md#paging).

Admission is [`messaging.list_messages`](messaging.list_messages.md)'s: the
caller's own mailbox, or the one `mailbox` names as a
[delegated read](../README.md#delegated-read), checked in the same order and
refused the same way. A refused caller receives no bytes. Local-only — queries
from the network are rejected, and so are queries carrying the `mcp` origin.
The operation stamps nothing read and tells no sender anything.

Rows are answered in ascending `Rev` order, each at its latest state. A row that
changed twice since `since` is answered once. Archived rows are answered: a row
put away, or taken back out, is a change. The operation answers at most `limit`
rows and reads one past the limit to set `More`.

The answer is one object followed by an `eos` object, or one `error_message`
object. A caller applies nothing it read before the `eos`: an object without
its `eos` is no answer.

## Arguments

* peer (string8) – Reads only the rows whose other party is this identity, from
  both boxes, as
  [`messaging.page_messages`](messaging.page_messages.md) reads them. Given as a
  hex public key or a name resolved via the directory.
* since (uint64) – Reads only rows whose `Rev` is above this one: the `Rev` of
  the first page a caller read, or the `NextRev` of an earlier answer. Defaults
  to 0, which reads from the start of the order.
* limit (uint64) – The most rows answered. 0 reads 50. A value over 100 is
  refused.
* generation (uint64) – The `Generation` of the answer that gave `since`.
  Required. A value that is not the mailbox's generation is refused.
* mailbox (string8) – As [`messaging.list_messages`](messaging.list_messages.md)
  takes it.

## Returned objects

Once the query is accepted, the operation checks again that this node hosts the
mailbox, then checks `since`, `limit` and `peer`'s resolution, reads the rows,
and checks `generation`, in that order. The first failure is the answer.

The operation returns one of:
* An `error_message` object reading `not a messaging participant` if this node
  stopped hosting the mailbox after the query was accepted.
* An `error_message` object reading
  `since is a position a previous answer gave you, not <since>` if `since` is
  over 9223372036854775807.
* An `error_message` object reading `limit is at most 100, not <limit>` if
  `limit` is over 100.
* An `error_message` object reading `unknown correspondent: <name>` if `peer`
  resolves to no identity.
* An `error_message` object reading `generation is required with a position` if
  `generation` is absent.
* An `error_message` object reading
  `generation changed: the mailbox was deleted since this position was read` if
  `generation` is not the mailbox's.
* An `error_message` object if the rows cannot be read.
* A [`messaging.message_changes`](../types/messaging.message_changes.md) object,
  followed by an `eos` object.

## Examples

```shellsession
$ astral-query messaging.list_message_changes -since 921 -generation 0 -out json
{"Type":"messaging.message_changes","Object":{"Messages":[{"Rev":924,"Envelope":{"Cursor":415,"ID":"0d41e6b28c5a4f9137be0a62d85c7f14","Box":"inbox","Sender":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Recipient":"026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2","ParentID":"7f3a1c9e5b024d6810af2e7c94b5d3a6","CreatedAt":"2026-09-02T22:16:40.215004Z","ArchivedAt":null,"ReadAt":"2026-09-02T22:17:03.811920Z","ReceiptDueAt":"2026-09-02T22:17:03.811920Z","ReceiptStoredAt":null,"LandedAt":null,"FailedAt":null,"FetchedAt":null,"Err":null}}],"NextRev":924,"More":false,"Generation":0}}
{"Type":"eos","Object":null}
```
