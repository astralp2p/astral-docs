# messaging.archive_result

Whether one call to [`messaging.archive`](../ops/messaging.archive.md) moved
the message it named.

**The field is `Changed` rather than `Archived`.** Under `undo` the second would
name the opposite of what happened: what the call reports is whether it was the
one that moved the message.

It is false alike for a message already where the caller asked and for one the
caller does not hold, which the caller acts on the same way. Separating them
would say whether an identifier the caller does not hold exists.

## Fields

* Changed (bool) – This call moved the message. False when the message was
  already where the caller asked, or the caller does not hold it.

## Example

```json
{
  "Type": "messaging.archive_result",
  "Object": {
    "Changed": true
  }
}
```
