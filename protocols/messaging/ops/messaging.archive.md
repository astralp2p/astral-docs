# messaging.archive

Archive one of the caller's messages, or restore it with `undo`. Archived mail
is excluded from inbox/outbox listings and waits; its original box is unchanged.
Archiving changes only this owner's copy and sends no notification.

Network and `mcp` origins are rejected first. The caller must have a
[hosted mailbox](../../../topics/mailbox-hosting.md#hosting); otherwise the query
is rejected without bytes.

## Arguments

* box (string8, required) – `inbox` or `outbox`.
* id (messaging.message_id, required) – Message ID as 32 hex characters, not an Object ID.
* undo (bool) – Restore instead of archive. Defaults to false.

## Returned objects

* A [`messaging.archive_result`](../types/messaging.archive_result.md). `Changed` is true when this call changes the state; false when already in that state or not held by the caller.
* An `error_message` reading `not a messaging participant` if hosting ended after acceptance.
* An `error_message` reading `box is inbox or outbox, not <box>` for an invalid box.
* An `error_message` if the row cannot be written.

## Examples

```shellsession
$ astral-query messaging.archive -box inbox -id 7f3a1c9e5b024d6810af2e7c94b5d3a6 -out json
{"Type":"messaging.archive_result","Object":{"Changed":true}}
```

```shellsession
$ astral-query messaging.archive -box inbox -id 7f3a1c9e5b024d6810af2e7c94b5d3a6 -undo true -out json
{"Type":"messaging.archive_result","Object":{"Changed":true}}
```
