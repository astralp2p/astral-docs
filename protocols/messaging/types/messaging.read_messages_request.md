# messaging.read_messages_request

What a caller asks
[`messaging.read_messages`](../ops/messaging.read_messages.md) to read: the
mailbox, the messages it names there, and how much of each one's direct replies
to answer beside it. Read from the operation's input stream.

**The mailbox is the caller's own unless the request names another.** A
`Mailbox` that is null, or that is the caller's own identity, reads the caller's
own mailbox. Any other identity makes the read a
[delegated read](../README.md#delegated-read): this node must host that mailbox,
the caller must hold
[`mod.messaging.read_mailbox_action`](mod.messaging.read_mailbox_action.md) for
it, and the read stamps nothing.

A repeated reference is dropped rather than refused, and the bound on a read
counts distinct messages. Charging a repeat twice would spend a budget the
caller cannot see.

## Fields

* Refs ([]messaging.message_ref) – The messages to read, each a
  [`messaging.message_ref`](messaging.message_ref.md) naming a box and an
  identifier. At least one and at most 20 distinct messages.
* Children (string8) – How much of each named message's direct replies the
  answer carries: `none` answers no replies, `envelopes` answers them without
  their bodies, and `full` answers them with their bodies. Empty means
  `envelopes`.
* MaxChildren (uint16) – How many replies of each named message the answer
  carries, oldest first. Zero means 10, and a value over 10 is clamped to 10.
* Mailbox (optional [identity](../../../primitive-types/identity.md)) – The
  mailbox to read. Null, or the caller's own identity, reads the caller's own
  mailbox. Another identity names a mailbox this node hosts that the caller is
  authorized to read.

## Example

```json
{
  "Type": "messaging.read_messages_request",
  "Object": {
    "Refs": [
      {"Box": "inbox", "ID": "7f3a1c9e5b024d6810af2e7c94b5d3a6"}
    ],
    "Children": "envelopes",
    "MaxChildren": 0,
    "Mailbox": null
  }
}
```
