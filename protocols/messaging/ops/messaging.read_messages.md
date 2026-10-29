# messaging.read_messages

Read message bodies and direct replies from the selected mailbox. An ordinary
read of the owner's inbox marks named messages read and reports collection;
`Children=full` also does so for inbox replies. `peek` and delegated reads
change no stamps and send no receipts.

A `network` or `mcp` query is answered `origin not allowed: <origin>`, and the
zero caller or the node identity is answered `not permitted`, before the request
is read. After the request arrives, hosting
is checked first; another mailbox also requires
[`mod.messaging.read_mailbox_action`](../types/mod.messaging.read_mailbox_action.md).
A denied [delegated read](../../../topics/mailbox-hosting.md#delegated-read)
closes without an answer. The reader need not have its own mailbox here.

Repeated reads claim no work. Bodies are bounded by `max_read_bytes` (65536 by
default); each named body is charged before its replies. Omitted bodies have
`Truncated` true. Read stamps and collection reports occur before that check,
even for omitted bodies, except under `peek` or a delegated read.

## Arguments

* peek (bool) – Read without stamps or receipts. Defaults to false.
* (stream) – One [`messaging.read_messages_request`](../types/messaging.read_messages_request.md).

## Returned objects

A [`messaging.read_messages_result`](../types/messaging.read_messages_result.md)
contains found messages, direct replies, and missing references. Missing
messages do not fail the batch. After mailbox checks, validation checks null
references, distinct-reference count, boxes, then `Children`.

Failures return `error_message`, except denied delegated reads:

| Error | Condition |
| --- | --- |
| `unexpected object: <type>` | Wrong input object type. |
| `not a messaging participant` | This node does not host the caller's own mailbox. |
| `a message ref names no message` | Null reference. |
| `name at least one message to read` | No references. |
| `name at most 20 messages in one read` | More than 20 distinct references. |
| `box is inbox or outbox, not <box>` | Invalid reference box. |
| `children is none, envelopes or full, not <children>` | Invalid reply mode. |

Invalid input streams and row-read or stamp failures also return `error_message`.

## Examples

```shellsession
$ echo '{"Type":"messaging.read_messages_request","Object":{"Refs":[{"Box":"inbox","ID":"7f3a1c9e5b024d6810af2e7c94b5d3a6"}],"Children":"none","MaxChildren":0,"Mailbox":null}}' \
    | astral-query messaging.read_messages -in json -out json
{"Type":"messaging.read_messages_result","Object":{"Messages":[{"Envelope":{"Cursor":412,"ID":"7f3a1c9e5b024d6810af2e7c94b5d3a6","Box":"inbox","Sender":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Recipient":"026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2","ParentID":"0d41e6b28c5a4f9137be0a62d85c7f14","CreatedAt":"2026-09-02T22:14:07.104829Z","ArchivedAt":null,"ReadAt":"2026-09-02T22:19:55.660411Z","ReceiptDueAt":null,"ReceiptStoredAt":null,"LandedAt":null,"FailedAt":null,"FetchedAt":null,"Err":null},"Content":"the index is rebuilt","ChildIDs":[],"Truncated":false}],"Replies":[],"NotFound":null}}
```

```shellsession
$ echo '{"Type":"messaging.read_messages_request","Object":{"Refs":[],"Children":"","MaxChildren":0,"Mailbox":null}}' \
    | astral-query messaging.read_messages -in json -out json
{"Type":"error_message","Object":"name at least one message to read"}
```
