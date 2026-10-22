# messaging.send_message

Send a message as the caller. The node writes the outbox before delivery and
answers when the recipient's node acknowledges storage or delivery fails.

Network and `mcp` origins are rejected first. The caller must have a
[hosted mailbox](../../../topics/mailbox-hosting.md#hosting); otherwise the
query is rejected without bytes. Sending also requires
[`mod.messaging.send_action`](../types/mod.messaging.send_action.md) for the
recipient. Denial returns `unknown recipient: <to>` and writes nothing.

After accepting the request, the node checks hosting, recipient, body size,
and parent before writing. [Message Delivery](../../../topics/message-delivery.md)
describes routing and receipts.

## Arguments

* (stream) – One [`messaging.send_message_request`](../types/messaging.send_message_request.md).

## Returned objects

A successful send returns a [`messaging.message_id`](../types/messaging.message_id.md),
shared by the outbox and inbox copies. Failures return `error_message`:

| Error | Condition |
| --- | --- |
| `not a messaging participant` | Hosting ended after acceptance or before the outbox write. |
| `unexpected object: <type>` | Wrong input object type. |
| `unknown recipient: <to>` | Unresolved or zero recipient, or denied send. |
| `content is over <n> bytes` | Body exceeds `max_payload_bytes` (65536 by default). |
| `cannot answer a message you do not hold` | Parent absent from both caller's boxes. |

These failures write no outbox row. Invalid input streams and storage failures
also return `error_message`.

After the outbox write, a delivery error reads `delivery failed: <cause>`:

| Cause | Outbox effect |
| --- | --- |
| `the recipient does not take messages from you` | Receive denied with code 5; `FailedAt` and `Err` set. |
| `the recipient took nothing; they may not exist, or their node may be unreachable` | No route or hosted recipient; `FailedAt` set, no `Err`. |
| `the message did not leave this node: <reason>` | Delivery write failed; `FailedAt` set. |
| `the recipient's node refused it: <words>` | Remote `error_message`; `FailedAt` and `Err` set. |
| `the message left and nothing came back: <reason>` | Outcome unknown; no delivery stamp. |

The last case includes timeout, connection loss, and an unexpected answer
(`answered <type>`). The recipient may have stored the message.
[Delivery errors](../../../topics/message-delivery.md#delivery) lists the
recipient's validation failures.

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
