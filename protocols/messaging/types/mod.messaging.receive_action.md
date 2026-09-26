# mod.messaging.receive_action

A [`mod.auth.action`](../../auth/types/mod.auth.action.md) requesting permission
for the actor to receive a message from another identity.

**The actor is the recipient, not the sender.** Every action type names what its
actor does, and receiving is the recipient's act. The distinction is not only a
name: the [`auth`](../../auth/README.md) protocol resolves an action it cannot
grant directly by walking the contracts the actor is subject to, so an action
naming the sender as actor would search the sender's delegations for a
permission the recipient holds.

What the sender is permitted to reach is a separate action,
[`mod.messaging.send_action`](mod.messaging.send_action.md). A message is stored
only when both are granted, and neither party's permission decides the other's.

The action is submitted where a delivery arrives — the recipient's node, for a
query addressed to an identity whose mailbox that node hosts — after the path,
provenance and hosting checks and before the query is accepted or anything is
read from it. A delivery that neither arrived over a link nor came from the
node's own send path is rejected before the action would be asked, so the
action is never the only check between an unasked send and an inbox — see
[Delivery](../README.md#delivery). A denied
delivery is rejected with `RejectNotAdmitted`, reject code 5. It is a separate
answer from `route_not_found`, which the node answers for an identity whose
mailbox it does not host: a sender turned away stops and asks whoever owns it,
and a sender that found nobody retries later. The sender reads the code as
`the recipient does not take messages from you` only when the recipient's
mailbox is on the sender's own node. Across nodes the sending node's relay path
answers the rejection as `route_not_found`, and the sender reads `the recipient
took nothing; they may not exist, or their node may be unreachable`. See
[Authorization](../README.md#authorization).

A grant of this action is not hosting authority, and hosting authority is not a
grant of this action: [`mod.messaging.host_mailbox_action`](mod.messaging.host_mailbox_action.md)
is a separate question, asked of the node first. See
[Hosting](../README.md#hosting).

A [`messaging.receipt`](messaging.receipt.md) asks no action. The sender's
outbox row is its permission.

Whether the action is granted is the [`auth`](../../auth/README.md) protocol's
decision — a registered handler, or an active
[`mod.auth.signed_contract`](../../auth/types/mod.auth.signed_contract.md)
whose permits include this action type. A node holding neither admits no
message.

A permit for this action carries no constraints. A permit whose `Constraints`
bundle is non-empty is refused rather than granted in full.

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID. ActorID is the recipient.
* FromID (identity) – The sender the actor is asking to receive from.

## Example

```json
{
  "Type": "mod.messaging.receive_action",
  "Object": {
    "Action": {
      "Nonce": "b2c3d4e5f6071829",
      "ActorID": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6"
    },
    "FromID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
  }
}
```
