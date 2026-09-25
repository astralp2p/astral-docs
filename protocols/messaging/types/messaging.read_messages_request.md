# messaging.read_messages_request

What a participant asks
[`messaging.read_messages`](../ops/messaging.read_messages.md) to read: the
messages it names, and how much of each one's direct replies to answer beside
it. Read from the operation's input stream.

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

## Example

```json
{
  "Type": "messaging.read_messages_request",
  "Object": {
    "Refs": [
      {"Box": "inbox", "ID": "7f3a1c9e5b024d6810af2e7c94b5d3a6"}
    ],
    "Children": "envelopes",
    "MaxChildren": 0
  }
}
```
