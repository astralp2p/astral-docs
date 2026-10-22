# mod.messaging.receive_action

Permission for `ActorID`, the recipient, to receive from `FromID`. The
recipient's node checks it after delivery provenance and hosting, before
accepting the message. Denial returns `RejectNotAdmitted` (code 5).

Send and receive permissions are separate. Nonempty permit constraints are
refused. See [Authorization](../../../topics/mailbox-hosting.md#authorization).

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID. ActorID is the recipient.
* FromID (identity) – The sender the actor is asking to receive from.

In JSON the embedded action's fields appear directly in the `Object` value,
beside `FromID`, not under an `Action` key.

## Example

```json
{
  "Type": "mod.messaging.receive_action",
  "Object": {
    "Nonce": "b2c3d4e5f6071829",
    "ActorID": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6",
    "FromID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
  }
}
```
