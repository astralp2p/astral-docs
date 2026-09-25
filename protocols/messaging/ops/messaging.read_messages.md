# messaging.read_messages

Read whole messages the caller holds, each named by box and identifier, with
each one's direct replies. Each inbox message the read names is stamped read, as
is each inbox reply when `Children` is `full`, and the sender of each is told
that the body was collected. Local-only — queries from the network are rejected,
and so are queries carrying the `mcp` origin.

This node must host the caller's mailbox. The query is rejected before
anything is read when the caller is the zero identity or this node does not host
the caller's mailbox, as [Hosting](../README.md#hosting) defines it, and a
refused caller receives no bytes. A query from the network or carrying the `mcp`
origin is rejected before the caller is checked.

Reading is not a claim. A second read answers the same messages unchanged, so a
caller that repeats a read whose answer it never saw loses nothing. The bodies
one answer carries are bounded by the module's `max_read_bytes`, 65536 by
default. A named message is charged against that bound before its replies, and
a body left out for room is marked `Truncated`. A message is stamped read and
its sender told of the collection as the row is read, before its body is
charged, so a message whose body is left out for room is stamped and reported
all the same.

Once the query is accepted, the operation reads the request, then checks again
that this node hosts the caller's mailbox, then checks the request in this
order: a null reference, the count of distinct references, each reference's
box, and `Children`. The first failure is the answer.

## Arguments

* (stream) – One
  [`messaging.read_messages_request`](../types/messaging.read_messages_request.md)
  naming the messages and how much of their replies to answer.

## Returned objects

The operation returns one of:
* An `error_message` object reading `unexpected object: <type>` if the input is
  an object of another type.
* An `error_message` object reading `not a messaging participant` if this node
  stopped hosting the caller's mailbox after the query was accepted.
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
* A `messaging.read_messages_result` object carrying the messages the caller
  holds, their replies, and the references it does not hold. A reference the
  caller does not hold is reported rather than refused.

## Examples

```shellsession
$ echo '{"Type":"messaging.read_messages_request","Object":{"Refs":[{"Box":"inbox","ID":"7f3a1c9e5b024d6810af2e7c94b5d3a6"}],"Children":"none","MaxChildren":0}}' \
    | astral-query messaging.read_messages -in json -out json
{"Type":"messaging.read_messages_result","Object":{"Messages":[{"Envelope":{"Cursor":412,"ID":"7f3a1c9e5b024d6810af2e7c94b5d3a6","Box":"inbox","Sender":"0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c","Recipient":"026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2","ParentID":"0d41e6b28c5a4f9137be0a62d85c7f14","CreatedAt":"2026-09-02T22:14:07.104829Z","ArchivedAt":null,"ReadAt":"2026-09-02T22:19:55.660411Z","ReceiptDueAt":null,"ReceiptStoredAt":null,"LandedAt":null,"FailedAt":null,"FetchedAt":null,"Err":null},"Content":"the index is rebuilt","ChildIDs":[],"Truncated":false}],"Replies":[],"NotFound":null}}
```

```shellsession
$ echo '{"Type":"messaging.read_messages_request","Object":{"Refs":[],"Children":"","MaxChildren":0}}' \
    | astral-query messaging.read_messages -in json -out json
{"Type":"error_message","Object":"name at least one message to read"}
```
