# messaging.read_message

A message returned by [`messaging.read_messages`](../ops/messaging.read_messages.md),
with metadata, an optional body, and direct reply IDs.

## Fields

* Envelope ([messaging.envelope](messaging.envelope.md)) – Message metadata.
* Content (optional string32) – Body; null for envelope-only replies or when omitted for space.
* ChildIDs ([]messaging.message_id) – All unarchived direct reply IDs, oldest first. Set on named messages; replies carry none.
* Truncated (bool) – Body omitted for space. False for envelope-only replies.

## Example

```json
{
  "Type": "messaging.read_message",
  "Object": {
    "Envelope": {
      "Cursor": 412,
      "ID": "7f3a1c9e5b024d6810af2e7c94b5d3a6",
      "Box": "inbox",
      "Sender": "0282fee8775757cdd8fda8b220195f5b8611312cd145c5a1a3aa55df210e779b2c",
      "Recipient": "026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2",
      "ParentID": "0d41e6b28c5a4f9137be0a62d85c7f14",
      "CreatedAt": "2026-09-02T22:14:07.104829Z",
      "ArchivedAt": null,
      "ReadAt": "2026-09-02T22:19:55.660411Z",
      "ReceiptDueAt": null,
      "ReceiptStoredAt": null,
      "LandedAt": null,
      "FailedAt": null,
      "FetchedAt": null,
      "Err": null
    },
    "Content": "the index is rebuilt",
    "ChildIDs": ["0196f3c2a8e47b1d9c05e3a7f2b64d18"],
    "Truncated": false
  }
}
```
