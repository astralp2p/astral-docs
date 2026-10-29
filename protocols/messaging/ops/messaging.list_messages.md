# messaging.list_messages

List a mailbox's envelopes without bodies or read effects. The default mailbox
is the caller's own; `mailbox` can select an authorized delegated read.

A `network` or `mcp` query is answered `origin not allowed: <origin>` first.
The node must host the selected mailbox. A delegated read checks the caller,
hosting, and
[`mod.messaging.read_mailbox_action`](../types/mod.messaging.read_mailbox_action.md)
in that order. A failed admission or an unresolved `mailbox` is answered with
an `error_message` reading `not permitted`; see
[Delegated read](../../../topics/mailbox-hosting.md#delegated-read).

The inbox is oldest first, except that `before`, or `limit` without `since`,
selects newest first. Outbox and archive are newest first. The smallest cursor
of a full page becomes the next `before`; a short page is the last.

## Arguments

* list (string8) – `inbox` (default), `outbox`, or `archive`. Archive includes both directions.
* from (string8) – Inbox sender, as a hex public key or directory name.
* to (string8) – Outbox recipient, as a hex public key or directory name.
* since (uint64) – Inbox rows after this cursor. Zero (default) applies no bound.
* unread_only (bool) – Inbox messages not yet read. Defaults to false.
* awaiting_pickup (bool) – Outbox messages stored by the recipient's node but not collected. Defaults to false.
* before (uint64) – Inbox/outbox rows below this cursor. Zero (default) applies no bound.
* limit (uint64) – Maximum rows, 1–100; zero (default) returns all matching rows.
* mailbox (string8) – Mailbox identity or directory name. Absent or naming the caller selects its own mailbox.

## Returned objects

A stream of [`messaging.envelope`](../types/messaging.envelope.md), followed by
`eos`. After acceptance, validation checks hosting, `since`, `before`, `limit`,
correspondent resolution, then list/filter combinations. The first failure
returns `error_message`:

| Error | Condition |
| --- | --- |
| `not a messaging participant` | Hosting ended after acceptance. |
| `since is a cursor a previous answer gave you, not <since>` | `since` exceeds 9223372036854775807. |
| `before is a cursor a previous answer gave you, not <before>` | `before` exceeds 9223372036854775807. |
| `limit is at most 100, not <limit>` | `limit` exceeds 100. |
| `since and before page in opposite directions` | Both cursors are nonzero. |
| `no such list: <list>` | Unknown list. |
| `unknown correspondent: <name>` | `from` or `to` does not resolve. |

Invalid filter combinations return `that filter does not apply to this list: <reason>`:

| Combination | Reason |
| --- | --- |
| Inbox + `awaiting_pickup` | `awaiting_pickup asks about what you sent` |
| Inbox + `to` | `an inbox is narrowed by from, not to` |
| Outbox + `since` | `since pages the inbox; the outbox is a history, read newest first` |
| Outbox + `unread_only` | `unread_only asks about what you received` |
| Outbox + `from` | `you are the sender of everything here; narrow by to` |
| Archive + `since` | `since pages the inbox; the archive is a history, read newest first` |
| Archive + `unread_only` or `awaiting_pickup` | `the archive spans both directions` |
| Archive + `from` or `to` | `the archive spans both directions, so neither from nor to picks one` |
| Archive + `before` | `before pages by cursor; the archive is read by time` |

Storage read failures also return `error_message`.

## Examples

```shellsession
$ astral-query messaging.list_messages -unread_only true -out json
{"Type":"messaging.envelope","Object":{"Cursor":412,"ID":"7f3a1c9e5b024d6810af2e7c94b5d3a6","Box":"inbox","Sender":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Recipient":"026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2","ParentID":"0d41e6b28c5a4f9137be0a62d85c7f14","CreatedAt":"2026-09-02T22:14:07.104829Z","ArchivedAt":null,"ReadAt":null,"ReceiptDueAt":null,"ReceiptStoredAt":null,"LandedAt":null,"FailedAt":null,"FetchedAt":null,"Err":null}}
{"Type":"eos","Object":null}
```

```shellsession
$ astral-query messaging.list_messages -list outbox -from scout -out json
{"Type":"error_message","Object":"that filter does not apply to this list: you are the sender of everything here; narrow by to"}
```
