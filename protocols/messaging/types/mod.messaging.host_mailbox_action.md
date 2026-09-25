# mod.messaging.host_mailbox_action

A [`mod.auth.action`](../../auth/types/mod.auth.action.md) requesting permission
for the actor, a node, to host the mailbox of another
[`Identity`](../../../core-definitions/identity.md).

The actor is the hosting node, and `MailboxID` is the identity whose mailbox it
hosts. The action asks one question: may this node host this identity's
mailbox. It names no correspondent and no operation. Who may write to whom is
[`mod.messaging.send_action`](mod.messaging.send_action.md) and
[`mod.messaging.receive_action`](mod.messaging.receive_action.md), and a
hosting permit answers neither.

**The mailbox identity is the root of the authority.** The
[`messaging`](../README.md) module gives the [`auth`](../../auth/README.md)
protocol one rule for this action: the action is granted when `MailboxID` is not
the zero identity and the actor is `MailboxID` itself. The rule is not
node-local, so a contract chain reaches it. A node holds the action through a
[`mod.auth.signed_contract`](../../auth/types/mod.auth.signed_contract.md) whose
issuer is the mailbox identity, whose subject is the node, and whose permits
include this action type: `auth` walks the contracts the node is subject to,
asks the action again with each issuer as actor, and the rule grants it for the
issuer that is `MailboxID`.

**A permit binds to its issuer's mailbox.** A contract from any other identity,
the node's own contract to itself included, grants nothing: its issuer is not
`MailboxID`, and the rule grants the action to `MailboxID` alone. No constraint
names the mailbox, and none is needed: the contract's issuer is the identity
whose mailbox it grants.

A [`mod.nodes.relay_for_action`](../../nodes/types/mod.nodes.relay_for_action.md)
permit from the same identity is a separate authority. It lets the node relay
traffic on the identity's behalf and grants no hosting, and a hosting permit
grants no relaying.

The action is submitted by the node that serves a mailbox, with the node's own
identity as actor, each time a request touching that mailbox starts: a delivery
or a receipt addressed to the identity, before it is accepted, and every mail
operation or direct call to the module acting on the mailbox, before anything
is read or written. See [Hosting](../README.md#hosting) for the contract
`messaging.create_identity` signs and the index that narrows which mailboxes a
node checks.

The permit in a hosting contract carries no constraints and has `Delegation` 0,
so the node hands the authority on to no other identity. A permit whose
`Constraints` bundle is non-empty is refused rather than granted in full,
whatever the bundle holds.

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID. ActorID is the hosting node.
* MailboxID (identity) – The identity whose mailbox the actor is asking to host.

## Example

```json
{
  "Type": "mod.messaging.host_mailbox_action",
  "Object": {
    "Action": {
      "Nonce": "c3d4e5f60718293a",
      "ActorID": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6"
    },
    "MailboxID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
  }
}
```
