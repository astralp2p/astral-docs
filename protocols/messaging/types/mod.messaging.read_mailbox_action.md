# mod.messaging.read_mailbox_action

A [`mod.auth.action`](../../auth/types/mod.auth.action.md) requesting permission
for the actor to read the mailbox of another
[`Identity`](../../../core-definitions/identity.md).

The actor is the reading identity, and `MailboxID` is the identity whose
mailbox it reads. The action asks one question: may this identity read this
mailbox. It names no message, no box and no correspondent. It grants reading
only: no sending, archiving or waiting, and no hosting, which is
[`mod.messaging.host_mailbox_action`](mod.messaging.host_mailbox_action.md).
Neither action grants the other.

**The authority decides.** The [`messaging`](../README.md) module gives the
[`auth`](../../auth/README.md) protocol no rule for this action, and being the
mailbox identity grants nothing. Whether the action is granted is the `auth`
protocol's decision: an `auth` handler registered for the action or the external
authority configured for it grants the action, and a node with neither refuses
every delegated read. The node asks the question with the reader as actor and
acts on the answer. It holds no rule about who reads whose mailbox, and the
reader presents its own identity and never the mailbox's credential.

**The action refuses every permit.** A
[`mod.auth.permit`](../../auth/types/mod.auth.permit.md) for this action is
refused whatever its `Constraints` bundle holds, an absent or empty bundle
included, and whatever its `Delegation`. No permit carries a delegated read, so
no [`mod.auth.signed_contract`](../../auth/types/mod.auth.signed_contract.md)
carries one: a chain link grants an action only through a permit that allows
it. In a contract whose subject is the reader, a permit for this action type
grants nothing, whoever the issuer is and whatever the authority would answer
about that issuer. `auth` therefore grants the action only through a
handler or the external authority asked about the reader itself.

The refusal covers contracts carrying this action and no other. A contract
carrying [`mod.auth.sudo_action`](../../auth/types/mod.auth.sudo_action.md) lets
its subject act as its issuer, and a read the subject makes as the issuer is the
issuer's read.

The action is submitted by the node that hosts the named mailbox, when
[`messaging.list_messages`](../ops/messaging.list_messages.md) or
[`messaging.read_messages`](../ops/messaging.read_messages.md) names a mailbox
other than the caller's own. The node first checks that the caller is neither
the zero identity nor the node itself, then that it hosts the named mailbox, and
asks the action last, before anything is read. It is never submitted for a read
of the caller's own mailbox. A refused reader reads nothing. See
[Delegated read](../README.md#delegated-read).

**A delegated read never stamps.** A read the action authorizes marks no inbox
message read, stamps no receipt due, sends no receipt, and stamps no collection
on a sender's outbox row on the same node — for the messages the read names and
for their replies under `Children` `full` alike. The mailbox's own reader finds
its mailbox exactly as it left it.

## Fields

* Action ([`mod.auth.action`](../../auth/types/mod.auth.action.md)) – The embedded base action carrying the Nonce and ActorID. ActorID is the reading identity.
* MailboxID (identity) – The identity whose mailbox the actor is asking to read.

## Example

```json
{
  "Type": "mod.messaging.read_mailbox_action",
  "Object": {
    "Action": {
      "Nonce": "d4e5f60718293a4b",
      "ActorID": "03a7c1f5b9d4e62a8f730ce15d2b4a9c11e8d77c3b5f04a6d92e1b8f72c4d3e5a6"
    },
    "MailboxID": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c"
  }
}
```
