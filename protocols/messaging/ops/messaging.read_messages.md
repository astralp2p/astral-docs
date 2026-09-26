# messaging.read_messages

Read whole messages from a mailbox, each named by box and identifier, with each
one's direct replies. The mailbox is the caller's own unless the request's
`Mailbox` names another. A read of the caller's own mailbox stamps each inbox
message it names read, as it does each inbox reply when `Children` is `full`,
and tells the sender of each that the body was collected. A
[delegated read](../README.md#delegated-read) of another identity's mailbox
stamps nothing and tells no sender anything. Local-only — queries from the
network are rejected, and so are queries carrying the `mcp` origin.

This node must host the mailbox read. A query from the network or carrying the
`mcp` origin is rejected before the caller is checked. The query is rejected
before it is accepted when the caller is the zero identity or this node's own
identity, and the caller receives no bytes. Every other check follows the
request, which arrives after the query is accepted.

When the request's `Mailbox` is null or names the caller, the mailbox is the
caller's own. The read is refused before any row is read when this node does
not host the caller's mailbox, as [Hosting](../README.md#hosting) defines it,
and the caller is answered `not a messaging participant`. The answer tells the
caller about its own mailbox alone.

When `Mailbox` names another identity, the read is a
[delegated read](../README.md#delegated-read). It is refused before any row is
read when this node does not host the named mailbox, or when
[`mod.messaging.read_mailbox_action`](../types/mod.messaging.read_mailbox_action.md)
is not granted with the caller as actor and the named mailbox as `MailboxID`,
checked in that order. A refused delegated read ends the query with no answer,
and its caller receives no bytes. The caller of a delegated read need not have a
mailbox on this node.

Reading is not a claim. A second read answers the same messages unchanged, so a
caller that repeats a read whose answer it never saw loses nothing. The bodies
one answer carries are bounded by the module's `max_read_bytes`, 65536 by
default. A named message is charged against that bound before its replies, and
a body left out for room is marked `Truncated`. In a read of the caller's own
mailbox, a message is stamped read and its sender told of the collection as the
row is read, before its body is charged, so a message whose body is left out
for room is stamped and reported all the same.

Once the query is accepted, the operation reads the request, then checks the
mailbox it names — for the caller's own, that this node hosts it; for another,
the delegated read's checks — then checks the request in this order: a null
reference, the count of distinct references, each reference's box, and
`Children`. The first failure is the answer, except for a refused delegated
read, which ends the query with no answer.

## Arguments

* (stream) – One
  [`messaging.read_messages_request`](../types/messaging.read_messages_request.md)
  naming the mailbox, the messages, and how much of their replies to answer.

## Returned objects

The operation returns one of:
* An `error_message` object reading `unexpected object: <type>` if the input is
  an object of another type.
* Nothing, and the query ends, if the request names another identity's mailbox
  and the delegated read is refused.
* An `error_message` object reading `not a messaging participant` if the
  request reads the caller's own mailbox and this node does not host it.
* An `error_message` object reading `a message ref names no message` if an
  entry of `Refs` is null.
* An `error_message` object reading `name at least one message to read` if the
  request names no message.
* An `error_message` object reading `name at most 20 messages in one read` if
  the request names more than 20 distinct messages.
* An `error_message` object reading `box is inbox or outbox, not <box>` if a
  reference names another box.
* An `error_message` object reading
  `children is none, envelopes or full, not <children>` if `Children` names
  another mode.
* An `error_message` object if the input is not one
  `messaging.read_messages_request`, or the rows cannot be read or stamped.
* A `messaging.read_messages_result` object carrying the messages the mailbox
  holds, their replies, and the references it does not hold. A reference the
  mailbox does not hold is reported rather than refused.

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
