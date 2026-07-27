# astrald.log.entry

A single log entry produced by the node.

## Fields

* Origin (identity) – Identity of the logger that produced the entry.
* Level (uint8) – Severity level; lower values are more severe.
* Time (time) – Timestamp when the entry was created.
* Objects (object[]) – Ordered list of typed objects that form the log message body.

## Example

```json
{
  "Type": "astrald.log.entry",
  "Object": {
    "Origin": "02bef8840eb35ef2ae3c83c07cb5779278904f99cb4103f71e37cc69931ae5e15f",
    "Level": 1,
    "Time": "2026-06-10T12:00:00Z",
    "Objects": [
      {"Type": "astrald.log.tag", "Object": "net"},
      {"Type": "string32", "Object": "link established"}
    ]
  }
}
```
