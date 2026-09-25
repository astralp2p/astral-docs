# messaging.list_messages

Stream one of the caller's three lists without the message bodies. A listing
hands no body out, so it stamps nothing read and tells no sender anything.
Local-only — queries from the network are rejected, and so are queries carrying
the `mcp` origin.

This node must host the caller's mailbox. The query is rejected before
anything is read when the caller is the zero identity or this node does not host
the caller's mailbox, as [Hosting](../README.md#hosting) defines it, and a
refused caller receives no bytes. A query from the network or carrying the `mcp`
origin is rejected before the caller is checked.

The list answers the caller's own rows and no other participant's. The inbox is
read in the order the node wrote the rows, oldest first; the outbox and the
archive are histories read newest first. The listing is not paged: its rows
carry no bodies, and the bound is on
[`messaging.read_messages`](messaging.read_messages.md), where the bodies are.

## Arguments

* list (string8) – Which list to read: `inbox` (what was written to the caller),
  `outbox` (what the caller wrote) or `archive` (what the caller put away, in
  either direction). Defaults to `inbox`.
* from (string8) – Inbox only. Lists only what this correspondent wrote, given
  as a hex public key or a name resolved via the directory.
* to (string8) – Outbox only. Lists only what the caller wrote to this
  correspondent, given as a hex public key or a name resolved via the directory.
* since (uint64) – Inbox only. Lists only the rows written after this cursor: the
  greatest `Cursor` of an earlier answer, or the `NextSince` of a
  [`messaging.wait_result`](../types/messaging.wait_result.md). Defaults to 0,
  which narrows nothing.
* unread_only (bool) – Inbox only. When true, lists only the messages whose body
  has not been handed out. Defaults to false.
* awaiting_pickup (bool) – Outbox only. When true, lists only the sends the
  recipient's node stored and has not handed out. Defaults to false.

## Returned objects

The operation returns one of:
* An `error_message` object reading `no such list: <list>` if `list` names none
  of the three.
* An `error_message` object reading
  `that filter does not apply to this list: <reason>` if a narrowing cannot
  apply to the named list. A narrowing is refused rather than ignored. The
  reason is one of:
  * `awaiting_pickup asks about what you sent` – `awaiting_pickup` on the inbox.
  * `an inbox is narrowed by from, not to` – `to` on the inbox.
  * `since pages the inbox; the outbox is a history, read newest first` –
    `since` on the outbox.
  * `unread_only asks about what you received` – `unread_only` on the outbox.
  * `you are the sender of everything here; narrow by to` – `from` on the
    outbox.
  * `since pages the inbox; the archive is a history, read newest first` –
    `since` on the archive.
  * `the archive spans both directions` – `unread_only` or `awaiting_pickup` on
    the archive.
  * `the archive spans both directions, so neither from nor to picks one` –
    `from` or `to` on the archive.
* An `error_message` object reading `unknown correspondent: <name>` if `from` or
  `to` resolves to no identity.
* An `error_message` object if the rows cannot be read.
* A stream of `messaging.envelope` objects, followed by an `eos` object.

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
