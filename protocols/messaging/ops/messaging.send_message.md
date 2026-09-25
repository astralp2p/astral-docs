# messaging.send_message

Send one message from the caller to another identity and return the identifier
it is stored under. The message is written to the caller's outbox before
delivery is attempted, then delivered as a `messaging.message` query to the
recipient's identity; the operation answers once the recipient's node has
stored it or the delivery has failed. Local-only — queries from the network are
rejected, and so are queries carrying the `mcp` origin.

This node must host the caller's mailbox. The query is rejected before
anything is read when the caller is the zero identity or this node does not host
the caller's mailbox, as [Hosting](../README.md#hosting) defines it, and a
refused caller receives no bytes. A query from the network or carrying the `mcp`
origin is rejected before the caller is checked.

The caller must also hold
[`mod.messaging.send_action`](../types/mod.messaging.send_action.md) for the
recipient. A send the action refuses is answered as one naming a recipient that
resolves to no identity, and no row is written.

## Arguments

* (stream) – One
  [`messaging.send_message_request`](../types/messaging.send_message_request.md)
  naming the recipient, the body, and the message it answers.

## Returned objects

The operation returns one of:
* An `error_message` object reading `unknown recipient: <to>` if `To` resolves
  to no identity, resolves to the zero identity, or names a recipient the
  caller may not reach. The three are one answer, and no row is written.
* An `error_message` object reading `content is over <n> bytes` if the body is
  longer than the module's `max_payload_bytes`, 65536 by default. No row is
  written.
* An `error_message` object reading `cannot answer a message you do not hold`
  if `ParentID` names a message the caller holds in neither box. No row is
  written.
* An `error_message` object reading `delivery failed: <cause>` if the outbox row
  was written and the delivery did not land. The cause is one of:
  * `the recipient does not take messages from you` – the recipient's node
    rejected the delivery with `RejectNotAdmitted`, code 5. The outbox row is
    stamped failed and carries these words.
  * `the recipient took nothing; they may not exist, or their node may be
    unreachable` – no node answered for the recipient: no node reached hosts
    the recipient's mailbox, or the node hosting it could not be reached. The
    outbox row is stamped failed.
  * `the message did not leave this node: <reason>` – the message could not be
    written to the delivery. The outbox row is stamped failed.
  * `the recipient's node refused it: <words>` – the recipient's node answered
    the delivery with an error, such as `message too large`,
    `the message answers one this node does not hold`, or
    `a message is already stored under that id`. The outbox row is stamped
    failed and carries these words.
  * `the message left and nothing came back: <reason>` – no acknowledgement
    came back: the delivery ran past the module's `delivery_timeout`, the
    connection closed before an answer, or the answer was neither an `ack` nor
    an error (`<reason>` then reads `answered <type>`). The recipient's node may
    have stored the message, and the outbox row is left unstamped.
* An `error_message` object if the input is not one
  `messaging.send_message_request`, or the outbox row cannot be written.
* A `messaging.message_id` object: the identifier the message is stored under,
  in the caller's outbox and the recipient's inbox alike. A later message names
  it as its `ParentID` to answer this one.

## Examples

```shellsession
$ echo '{"Type":"messaging.send_message_request","Object":{"To":"scout","Content":"the index is rebuilt","ParentID":"0d41e6b28c5a4f9137be0a62d85c7f14"}}' \
    | astral-query messaging.send_message -in json -out json
{"Type":"messaging.message_id","Object":"7f3a1c9e5b024d6810af2e7c94b5d3a6"}
```

```shellsession
$ echo '{"Type":"messaging.send_message_request","Object":{"To":"nobody","Content":"hello","ParentID":"00000000000000000000000000000000"}}' \
    | astral-query messaging.send_message -in json -out json
{"Type":"error_message","Object":"unknown recipient: nobody"}
```
