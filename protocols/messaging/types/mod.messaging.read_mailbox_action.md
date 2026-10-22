# mod.messaging.read_mailbox_action

Permission for `ActorID` to list and read `MailboxID`'s mail without changing
read or collection stamps. It grants no sending, waiting, or archiving.

The action has no built-in grant and refuses every permit. An `auth` handler or
external authority must grant it to the reader. It is checked only for a
[delegated read](../../../topics/mailbox-hosting.md#delegated-read), after
hosting is checked.

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID. ActorID is the reading identity.
* MailboxID (identity) – The identity whose mailbox the actor is asking to read.

In JSON the embedded action's fields appear directly in the `Object` value,
beside `MailboxID`, not under an `Action` key.

## Example

```json
{
  "Type": "mod.messaging.read_mailbox_action",
  "Object": {
    "Nonce": "d4e5f60718293a4b",
    "ActorID": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6",
    "MailboxID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
  }
}
```
