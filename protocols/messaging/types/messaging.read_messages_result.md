# messaging.read_messages_result

The result of [`messaging.read_messages`](../ops/messaging.read_messages.md).
Replies are one level deep; each reply's `ParentID` identifies its parent.
Missing references do not fail the batch. Read effects and byte limits are
specified by the operation.

## Fields

* Messages ([]messaging.read_message) – Found messages, in reference order.
* Replies ([]messaging.read_message) – Unarchived direct replies, oldest first per named message, limited by `MaxChildren`. Empty when `Children` is `none`.
* NotFound ([]messaging.message_ref) – References absent from the selected mailbox.

## Example

```json
{
  "Type": "messaging.read_messages_result",
  "Object": {
    "Messages": [
      {
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
        "ChildIDs": [],
        "Truncated": false
      }
    ],
    "Replies": [],
    "NotFound": [
      {
        "Box": "inbox",
        "ID": "0d41e6b28c5a4f9137be0a62d85c7f14"
      }
    ]
  }
}
```
