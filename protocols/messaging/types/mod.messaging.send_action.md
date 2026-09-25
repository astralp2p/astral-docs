# mod.messaging.send_action

A [`mod.auth.action`](../../auth/types/mod.auth.action.md) requesting permission
for the actor to send a message to another identity.

The actor is the sending participant, and the action asks what that participant
is permitted to reach. What the recipient is permitted to receive is a separate
action, [`mod.messaging.receive_action`](mod.messaging.receive_action.md). A
message is stored only when both are granted, and neither party's permission
decides the other's.

The action is submitted where a send starts — the
[`messaging`](../README.md) module, reached by
[`messaging.send_message`](../ops/messaging.send_message.md) and by the
`send_message` tool of the [`mcp`](../../mcp/README.md) endpoint alike — after
the module finds that it hosts the sender's mailbox and before anything is
written. A denied sender is answered as it is for a recipient that
resolves to no [`Identity`](../../../core-definitions/identity.md),
`unknown recipient`, and no row is written: it learns that it cannot reach the
recipient, and not whether the recipient exists.

Whether the action is granted is the [`auth`](../../auth/README.md) protocol's
decision — a registered handler, or an active
[`mod.auth.signed_contract`](../../auth/types/mod.auth.signed_contract.md)
whose permits include this action type. A node holding neither denies every
send.

A permit for this action carries no constraints. A permit whose `Constraints`
bundle is non-empty is refused rather than granted in full.

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID. ActorID is the sending participant.
* ToID (identity) – The recipient the actor is asking to send to.

## Example

```json
{
  "Type": "mod.messaging.send_action",
  "Object": {
    "Action": {
      "Nonce": "a1b2c3d4e5f60718",
      "ActorID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
    },
    "ToID": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6"
  }
}
```
