# mod.messaging.host_mailbox_action

Permission for `ActorID` to host `MailboxID`'s mailbox. The root rule grants
this action to the nonzero `MailboxID` itself; a hosting contract delegates it
to the node. Nonempty permit constraints are refused.

[Mailbox Hosting](../../../topics/mailbox-hosting.md#hosting) defines the
contract and index checks. This action grants no relay, send, receive, or
mailbox-read permission.

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID. ActorID is the hosting node.
* MailboxID (identity) – The identity whose mailbox the actor is asking to host.

In JSON the embedded action's fields appear directly in the `Object` value,
beside `MailboxID`, not under an `Action` key.

## Example

```json
{
  "Type": "mod.messaging.host_mailbox_action",
  "Object": {
    "Nonce": "c3d4e5f60718293a",
    "ActorID": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6",
    "MailboxID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
  }
}
```
