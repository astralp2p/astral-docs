# messaging.archive_result

The result of [`messaging.archive`](../ops/messaging.archive.md).

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
