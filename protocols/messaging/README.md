# messaging

The `messaging` protocol carries mail between identities. A node hosts each
participant's inbox and outbox under a contract from that identity. Delivery
stores mail even while the recipient's client is offline.

A send requires permission from both sides: the sender may send to the
recipient, and the recipient may receive from the sender. Hosting alone grants
neither. Participants use their apphost access tokens to reach their mail;
[`mcp`](../mcp/README.md) exposes the same mailbox behavior as tools.

## Operations

* [`messaging.create_mailbox`](ops/messaging.create_mailbox.md) – create an identity, mailbox, and access token.
* [`messaging.mailbox`](ops/messaging.mailbox.md) – read a mailbox record without credentials.
* [`messaging.delete_mailbox`](ops/messaging.delete_mailbox.md) – remove a mailbox and its local mail.
* [`messaging.send_message`](ops/messaging.send_message.md) – send a body to an identity or alias.
* [`messaging.list_messages`](ops/messaging.list_messages.md) – list inbox, outbox, or archived envelopes.
* [`messaging.read_messages`](ops/messaging.read_messages.md) – read bodies and direct replies.
* [`messaging.wait`](ops/messaging.wait.md) – wait for matching inbox mail without marking it read.
* [`messaging.archive`](ops/messaging.archive.md) – archive a message or restore it.

Operations reject network and MCP-origin queries. Mail operations use the
caller's own mailbox; listing and reading also allow an authorized delegated
read. The `messaging.message` and `messaging.receipt` queries carry deliveries
and collection reports between nodes.

## Topics

* [Messaging](../../topics/messaging.md) – mailbox use, replies, cursors, and configuration.
* [Mailbox Hosting](../../topics/mailbox-hosting.md) – contracts, access, expiry, and deletion.
* [Message Delivery](../../topics/message-delivery.md) – routing, delivery results, and receipts.
