# messaging.read_messages_request

The input to [`messaging.read_messages`](../ops/messaging.read_messages.md).
Repeated `(Box, ID)` references are removed before checking the count.
A [delegated read](../../../topics/mailbox-hosting.md#delegated-read) selects
another mailbox and changes no read or collection stamps.

## Fields

* Refs ([]messaging.message_ref) – 1–20 distinct [box-and-ID references](messaging.message_ref.md), with no null entries.
* Children (string8) – `none`, `envelopes`, or `full`; empty means `envelopes`.
* MaxChildren (uint16) – Replies per named message, oldest first. Zero means 10; values over 10 are clamped to 10.
* Mailbox (optional [identity](../../../primitive-types/identity.md)) – Mailbox to read. Null or the caller's identity selects its own; another identity requires delegated-read authority.

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
