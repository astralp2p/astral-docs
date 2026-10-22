# mod.messaging.send_action

Permission for `ActorID`, the sender, to send to `ToID`. The sending node
checks it after hosting, before writing the outbox. Denial returns
`unknown recipient: <to>` and writes nothing.

Send and receive permissions are separate. Nonempty permit constraints are
refused. See [Authorization](../../../topics/mailbox-hosting.md#authorization).

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID. ActorID is the sending participant.
* ToID (identity) – The recipient the actor is asking to send to.

In JSON the embedded action's fields appear directly in the `Object` value,
beside `ToID`, not under an `Action` key.

## Example

```json
{
  "Type": "mod.messaging.send_action",
  "Object": {
    "Nonce": "a1b2c3d4e5f60718",
    "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
    "ToID": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6"
  }
}
```
