# messaging.archive

Put one of the caller's messages away, or put it back with `undo`, and report
whether this call moved it. A message put away is excluded from the inbox and
outbox listings and never answered by `messaging.wait` again; one put back is
answered by both again. Local-only — queries from the network are rejected, and
so are queries carrying the `mcp` origin.

This node must host the caller's mailbox. The query is rejected before
anything is read when the caller is the zero identity or this node does not host
the caller's mailbox, as [Hosting](../README.md#hosting) defines it, and a
refused caller receives no bytes. A query from the network or carrying the `mcp`
origin is rejected before the caller is checked.

Archiving is the caller's own bookkeeping: it names no other node, crosses no
link, and the other party learns nothing from it.

## Arguments

* box (string8, required) – `inbox` or `outbox`: the box the message sits in, as
  an envelope reported it.
* id (messaging.message_id, required) – The message's identifier, as thirty-two
  hexadecimal characters. It names a
  [`messaging.message_id`](../types/messaging.message_id.md), not an Object ID.
* undo (bool) – When true, puts the message back instead. Defaults to false.

## Returned objects

The operation returns one of:
* An `error_message` object reading `box is inbox or outbox, not <box>` if
  `box` names neither.
* An `error_message` object if the row cannot be written.
* A `messaging.archive_result` object whose `Changed` is true when this call
  moved the message, and false when the message was already where the caller
  asked or the caller does not hold it.

## Examples

```shellsession
$ astral-query messaging.archive -box inbox -id 7f3a1c9e5b024d6810af2e7c94b5d3a6 -out json
{"Type":"messaging.archive_result","Object":{"Changed":true}}
```

```shellsession
$ astral-query messaging.archive -box inbox -id 7f3a1c9e5b024d6810af2e7c94b5d3a6 -undo true -out json
{"Type":"messaging.archive_result","Object":{"Changed":true}}
```
